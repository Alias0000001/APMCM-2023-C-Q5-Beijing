"""Audit-02 independent structural stress. No re-estimation of reference observations."""
import csv,itertools,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h.split(","));w.writerows([[f"{x:.9f}" if isinstance(x,(int,float)) else x for x in r] for r in rows])
A={r["parameter"]:float(r["value"]) for r in read("R9_7A_CONTEST_ACTIVITY_INPUTS.csv")}
E={r["parameter"]:float(r["value"]) for r in read("R9_7B_ENERGY_INPUTS.csv")}
M={r["source_id"]:float(r["factor_value"])*1e6/float(r["lifetime_km"]) for r in read("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv")}
F={r["technology"]:r for r in read("R9_7E_ROAD_FACTORS.csv") if r["standard"]=="V"}
V=A["private_small_micro_cars"]*A["target_population"]/A["reference_population"]*A["private_daily_distance"]*A["central_city_dispatch_rate"]*365
B=A["bus_vkt"]*A["target_population"]/A["reference_population"]
def ac(k):return E[k+"_off"]+(E[k+"_on"]-E[k+"_off"])*E["ac_share"]
def f(k,j):return float(F[k][j])
gas=E["gasoline_l100"]/100*E["gasoline_mj_l"]
pe=E["phev_cd_e"]*E["uf"]/E["eta"];pg=E["phev_cs_l100"]/100*E["gasoline_mj_l"]*(1-E["uf"])
ce=E["car_e"]/E["eta"];be=E["bus_e"]/E["eta"];ge=E["cng_ef"]*(1-E["lng_share"])+E["lng_ef"]*E["lng_share"]
# Per vehicle-km: final MJ, fuel WTW g, electricity WTW g, production g, road NOx g, road PM2.5 g.
tech=[
 [gas,gas*E["gasoline_ef"],0,M["QIAO17_ICE"],f("private_gasoline","NOx"),f("private_gasoline","PM2_5")],
 [ce*3.6,0,ce*E["grid_ef"]*1000,M["QIAO17_BEV_NMC"],0,0],
 [pg+pe*3.6,pg*E["gasoline_ef"],pe*E["grid_ef"]*1000,M["XIONG19_PHEV_NMC"],f("private_gasoline","NOx")*(1-E["uf"]),f("private_gasoline","PM2_5")*(1-E["uf"])],
 [ac("diesel"),ac("diesel")*E["diesel_ef"],0,M["LIN15_BUS_CDB"],f("bus_diesel","NOx"),f("bus_diesel","PM2_5")],
 [ac("gas"),ac("gas")*ge,0,M["LIN15_BUS_NGB"],f("bus_natural_gas","NOx"),f("bus_natural_gas","PM2_5")],
 [ac("hybrid"),ac("hybrid")*E["diesel_ef"],0,M["LIN15_BUS_DHEB"],f("bus_diesel","NOx"),f("bus_diesel","PM2_5")],
 [be*3.6,0,be*E["grid_ef"]*1000,M["LIN15_BUS_BEB"],0,0]]
d,g,n,h=[A[k] for k in ("bus_diesel_count","bus_gas_count","bus_total_count","bus_mixed_count")]
u=n-d-g-h;ud=d/(d+g)
ss=["S-1","S0","S1","S2","S3","S4"]
def norm(v):
    assert min(v)>=0 and sum(v)>0
    return [x/sum(v) for x in v]
def run(s,t,q,rc,rb,fossil="mix",urban=1):
    c=norm([1-s,s*t*rc,s*(1-t)*rc]);b=norm([d+u*ud,g+u*(1-ud),h*(1-q),h*q*rb])
    cf=[1,0,0];bf=[1,0,0,0] if fossil=="diesel" else [ud,1-ud,0,0];cb=[0,1,0];bb=[0,0,0,1]
    out=[]
    for i,(x,y) in enumerate([(cf,bf),(c,b),(c,bb),(cb,b),(cb,bb),(cb,bb)]):
        assert math.isclose(sum(x),1) and math.isclose(sum(y),1)
        v=[*[k*V*urban for k in x],*[k*B*urban for k in y]]
        G=A["S4_grid_factor_multiplier"] if i==5 else 1
        def total(fn):return sum(x*fn(k) for x,k in zip(v,tech))
        out.append([ss[i],c[1],c[2],b[3],total(lambda k:k[0])/1e9,total(lambda k:k[1]+k[2]*G)/1e9,total(lambda k:k[3])/1e9,total(lambda k:k[1]+k[2]*G+k[3])/1e9,total(lambda k:k[4])/1e6,total(lambda k:k[5])/1e6])
    return out
ref=(A["private_nev_share"],A["private_bev_fraction_of_nev"],A["bus_bev_fraction_of_mixed"],1,1)
base=run(*ref)
z=read("R9_7E_ENVIRONMENTAL_MATRIX.csv")
for r,s in zip(base,z):
    assert r[0]==s["scenario"]
    for j,k in [(4,"final_energy_PJ"),(5,"WTW_GWP_kt_y"),(6,"production_GWP_kt_y"),(7,"partial_GWP_kt_y"),(8,"road_NOx_t_y"),(9,"road_PM2_5_t_y")]:
        assert math.isclose(r[j],float(s[k]),rel_tol=0,abs_tol=2e-6),(k,r[j],s[k])
rows=[];bus_nox=0
for pars in itertools.product([.05,.08,.1158],[.6,.778,.9],[.6,.8,1],[.8,1,1.2],[.8,1,1.2]):
    rr=run(*pars);z0=rr[1][7]
    for r in rr:rows.append([*pars,*r,100*(1-r[7]/z0)])
    assert math.isclose(rr[4][7]-rr[3][7]-rr[2][7]+rr[1][7],0,abs_tol=1e-8)
    bus_nox+=rr[2][8]<rr[3][8]
alt=run(*ref,fossil="diesel")
urb=run(*ref,urban=A["reference_population"]/A["reference_urban_population"])
alternatives=[[name,*r,100*(1-r[7]/rr[1][7])] for name,rr in [("base",base),("all_diesel_Sminus1",alt),("urban_numerator_all_assigned_stress",urb)] for r in rr]
env=[]
for s in ss:
    rr=[r for r in rows if r[5]==s];y=[r[12] for r in rr];pr=[r[15] for r in rr];env.append([s,min(y),max(y),min(pr),max(pr),len(rr)])
assert len(rows)==1458 and all(r[1:]==s[1:] for r,s in zip(base[1:],alt[1:]))
write("R9_7AUDIT02_PROPULSION_GRID.csv","private_NEV_stock_share,BEV_fraction_of_NEV,mixed_bus_BEV_fraction,NEV_relative_mileage,BEV_bus_relative_mileage,scenario,S0_car_BEV_VKT_share,S0_car_PHEV_VKT_share,S0_bus_BEV_VKT_share,energy_PJ,WTW_kt,production_kt,partial_GWP_kt,NOx_t,PM2_5_t,paired_reduction_pct",rows)
write("R9_7AUDIT02_ALTERNATIVES.csv","case,scenario,S0_car_BEV_VKT_share,S0_car_PHEV_VKT_share,S0_bus_BEV_VKT_share,energy_PJ,WTW_kt,production_kt,partial_GWP_kt,NOx_t,PM2_5_t,paired_reduction_pct",alternatives)
write("R9_7AUDIT02_PROPULSION_ENVELOPE.csv","scenario,min_partial_GWP_kt,max_partial_GWP_kt,min_paired_reduction_pct,max_paired_reduction_pct,sets",env)
print("PASS: 243 paired propulsion sets; independent baseline and additive identity; bus-first NOx sets",bus_nox)
