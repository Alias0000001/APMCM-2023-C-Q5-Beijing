"""Independent six-scenario audit; no import of production model code.
Rebuild from input registers, compare separately with archived outputs.
"""
import csv, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/"02_Cleaned_Data"
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def rows(n):return read(D/n)
def pmap(n):return {x["parameter"]:float(x["value"]) for x in rows(n)}
def find(a,**kw):return next(x for x in a if all(x[k]==v for k,v in kw.items()))
a=pmap("R9_7A_CONTEST_ACTIVITY_INPUTS.csv"); e=pmap("R9_7B_ENERGY_INPUTS.csv")
V=a["target_population"]/a["reference_population"]*a["private_small_micro_cars"]*a["private_daily_distance"]*365*a["central_city_dispatch_rate"]*a["ownership_transfer"]*a["mileage_transfer"]
B=a["target_population"]/a["reference_population"]*a["bus_vkt"]*a["bus_supply_transfer"]
p=a["private_nev_share"]; t=a["private_bev_fraction_of_nev"]; q=a["bus_bev_fraction_of_mixed"]
d=a["bus_diesel_count"]; g=a["bus_gas_count"]; m=a["bus_mixed_count"]; n=a["bus_total_count"]
u=n-d-g-m; rho=d/(d+g)
car0=[V*(1-p),V*p*t,V*p*(1-t)];bus0=[B*d/n,B*g/n,B*m*(1-q)/n,B*m*q/n,B*u/n]
allcar=[0,V,0];allbus=[0,0,0,B,0]
sc={"S-1":([V,0,0],[B*rho,B*(1-rho),0,0,0],1),"S0":(car0,bus0,1),"S1":(car0,allbus,1),"S2":(allcar,bus0,1),"S3":(allcar,allbus,1),"S4":(allcar,allbus,a["S4_grid_factor_multiplier"])}
A=rows("R9_7A_SIX_SCENARIO_VKT.csv");E=rows("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv");G=rows("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv");F=rows("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv");P=rows("R9_7E_ROAD_FACTORS.csv");O=rows("R9_7E_ROAD_POLLUTANT_SCENARIOS.csv");W=rows("R9_7AUDIT04_WEAR_FACTORS.csv");Z=rows("R9_7AUDIT04_WEAR_SCENARIOS.csv");K=rows("R9_7AUDIT04_BATTERY_CAPACITY.csv");S=rows("R9_7D_SERVICE_SENSITIVITY.csv")
L={x["parameter_id"]:float(x["value"]) for x in read(R/"07_LCA_LCIA"/"R9_LCI_PARAMETER_LEDGER.csv") if x["parameter_id"] in {"R9_BEV_CAPACITY_PROXY","R9_PHEV_CAPACITY_PROXY","R9_PRIVATE_LIFETIME_VKT"}}
checks=[]
def ck(s,k,x,y):
    y=float(y);tol=max(1e-5,abs(y)*1e-9);err=abs(x-y);checks.append([s,k,x,y,err,tol,"PASS" if err<=tol else "FAIL"])
def group(s,table,calc):
    for k,v in calc.items():ck(s,k,v,table[k])
def rate(key):
    z=find(F,source_id=key);return float(z["factor_value"])/float(z["lifetime_km"])
def ac(k):return e[k+"_off"]*(1-e["ac_share"])+e[k+"_on"]*e["ac_share"]
tot={}
for s,(c,b,h) in sc.items():
    i,j,k=c; bd,bg,bh,be,bu=b; dd=bd+bu*rho;gg=bg+bu*(1-rho)
    group(s,find(A,scenario=s),dict(zip(["private_total_vkt_km","bus_total_vkt_km","private_ICEV_vkt_km","private_BEV_vkt_km","private_PHEV_vkt_km","bus_diesel_vkt_km","bus_natural_gas_vkt_km","bus_mixed_nonBEV_vkt_km","bus_BEV_vkt_km","bus_unclassified_vkt_km","operating_grid_factor_multiplier"],[sum(c),sum(b),*c,*b,h])))
    l=(i*e["gasoline_l100"]+k*(1-e["uf"])*e["phev_cs_l100"])/100
    dm=dd*ac("diesel")+bh*ac("hybrid");gm=gg*ac("gas")
    ce=(j*e["car_e"]+k*e["uf"]*e["phev_cd_e"])/e["eta"];bee=be*e["bus_e"]/e["eta"]
    wg=l*e["gasoline_mj_l"]*e["gasoline_ef"]/1e6;wd=dm*e["diesel_ef"]/1e6;wn=gm*((1-e["lng_share"])*e["cng_ef"]+e["lng_share"]*e["lng_ef"])/1e6
    wc=ce*e["grid_ef"]*h/1000;wb=bee*e["grid_ef"]*h/1000
    cw=wg+wc;bw=wd+wn+wb
    group(s,find(E,scenario=s,case="base"),{"gasoline_L":l,"diesel_MJ":dm,"natural_gas_MJ":gm,"private_electricity_kWh":ce,"bus_electricity_kWh":bee,"final_energy_MJ":l*e["gasoline_mj_l"]+dm+gm+(ce+bee)*3.6,"gasoline_WTW_tCO2e":wg,"diesel_WTW_tCO2e":wd,"natural_gas_WTW_tCO2e":wn,"private_electricity_WTW_tCO2e":wc,"bus_electricity_WTW_tCO2e":wb,"private_WTW_tCO2e":cw,"bus_WTW_tCO2e":bw,"total_WTW_tCO2e":cw+bw})
    cm=sum(v*rate(f) for v,f in zip(c,["QIAO17_ICE","QIAO17_BEV_NMC","XIONG19_PHEV_NMC"]))
    bm=sum(v*rate(f) for v,f in zip([dd,gg,bh,be],["LIN15_BUS_CDB","LIN15_BUS_NGB","LIN15_BUS_DHEB","LIN15_BUS_BEB"]))
    total=cm+bm+cw+bw;tot[s]=total
    group(s,find(G,scenario=s),{"private_vehicle_production_GWP_t_y":cm,"bus_manufacturing_GWP_t_y":bm,"total_manufacturing_GWP_t_y":cm+bm,"WTW_operating_GWP_t_y":cw+bw,"partial_LCA_GWP_t_y":total})
    svc=find(S,scenario=s,case="reference");cp=V*float(svc["car_occupancy_proxy"]);bp=a["target_population"]/a["reference_population"]*a["bus_boardings"]*float(svc["bus_trip_km_proxy"])
    group(s,svc,{"car_PKM":cp,"bus_PKM":bp,"car_partial_GWP_g_per_VKT":(cw+cm)*1e6/V,"bus_partial_GWP_g_per_VKT":(bw+bm)*1e6/B,"car_partial_GWP_g_per_PKM":(cw+cm)*1e6/cp,"bus_partial_GWP_g_per_PKM":(bw+bm)*1e6/bp})
    for pol in ["CO","VOCs","NOx","PM2_5","PM10"]:
        f=lambda tech:float(find(P,standard="V",technology=tech)[pol])
        pc=(i+k*(1-e["uf"]))*f("private_gasoline")/1e6;pb=((dd+bh)*f("bus_diesel")+gg*f("bus_natural_gas"))/1e6
        row=find(O,case="V_reference",scenario=s,pollutant=pol)
        for key,v in [("private_t_y",pc),("bus_t_y",pb),("total_t_y",pc+pb)]:ck(s,pol+"_"+key,v,row[key])
        if pol.startswith("PM"):
            wc2=V*float(find(W,factor_case="EEA_generic",vehicle="car",pollutant=pol)["sum_g_per_km"])/1e6
            wb2=B*float(find(W,factor_case="EEA_generic",vehicle="bus",pollutant=pol)["sum_g_per_km"])/1e6
            ck(s,pol+"_covered_road_PM_t_y",pc+pb+wc2+wb2,find(Z,case="EEA_equal",scenario=s,pollutant=pol)["covered_road_PM_t_y"])
    kj=j*L["R9_BEV_CAPACITY_PROXY"]/L["R9_PRIVATE_LIFETIME_VKT"];kk=k*L["R9_PHEV_CAPACITY_PROXY"]/L["R9_PRIVATE_LIFETIME_VKT"]
    group(s,find(K,scenario=s),{"BEV_capacity_kWh_y":kj,"PHEV_capacity_kWh_y":kk,"total_capacity_kWh_y":kj+kk})
ck("ALL","fixed_VKT_interaction_t",tot["S3"]-tot["S2"]-tot["S1"]+tot["S0"],0)
with (D/"R9_7FIX_INDEPENDENT_CHECKS.csv").open("w",newline="",encoding="utf8") as f:
    w=csv.writer(f);w.writerow(["scenario","metric","independent","stored","absolute_error","tolerance","status"]);w.writerows(checks)
bad=[x for x in checks if x[-1]=="FAIL"]
print(f"Independent checks: {len(checks)-len(bad)}/{len(checks)} passed")
if bad:raise AssertionError(bad[:12])
