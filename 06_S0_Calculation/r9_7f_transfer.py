"""Deterministic paired transfer stress, not a probability model."""
import csv,itertools,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h.split(","));w.writerows([[f"{x:.9f}" if isinstance(x,(float,int)) else x for x in r] for r in rows])
ss=["S-1","S0","S1","S2","S3","S4"];pol=["CO","VOCs","NOx","PM2_5","PM10"]
e=read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv");m=read("R9_7C_PARTIAL_LCA_GWP_SOURCE_SENSITIVITY.csv");p=read("R9_7E_ROAD_POLLUTANT_SCENARIOS.csv")
E={(r["case"],r["scenario"]):r for r in e};M={(r["factor_set"],r["scenario"]):r for r in m};P={(r["case"],r["scenario"],r["pollutant"]):r for r in p}
ec=list(dict.fromkeys(r["case"] for r in e));ms=list(dict.fromkeys(r["factor_set"] for r in m));pc=list(dict.fromkeys(r["case"] for r in p))
levels=[.8,1,1.2];grid=list(itertools.product(levels,repeat=3))
def climate(s,g,d,b,den=1,energy="base",prod="QIAO2017_BEV_NMC",lc=150000,lb=400000):
    x=E[energy,s];y=M[prod,s];a=g*d*den
    cw=a*float(x["private_WTW_tCO2e"]);bw=b*float(x["bus_WTW_tCO2e"])
    cm=a*float(y["private_vehicle_production_GWP_t_y"])*150000/lc
    bm=b*float(y["bus_manufacturing_GWP_t_y"])*400000/lb
    return [cw,bw,cm,bm,cw+bw+cm+bm]
def road(s,g,d,b,den,k,cs="V_reference"):
    r=P[cs,s,k];return g*d*den*float(r["private_t_y"])+b*float(r["bus_t_y"])
def transfer(cases):
    rows=[]
    for g,d,b in cases:
        z=climate("S0",g,d,b)[4]
        for s in ss:
            c=climate(s,g,d,b);rows.append([g,d,b,s,*c,100*(1-c[4]/z),*[road(s,g,d,b,1,k) for k in pol]])
    return rows
base=transfer(grid);diag=transfer([(1.171038,d,.646917) for d in levels])
worst=None
stats={};counts={"gwp":[0,0],"nox":[0,0,0],"pm":[0,0,0]}
def add(layer,s,k,x,b):
    a=stats.setdefault((layer,s,k),[math.inf,-math.inf,math.inf,-math.inf,0]);r=100*(1-x/b)
    a[:]=[min(a[0],x),max(a[1],x),min(a[2],r),max(a[3],r),a[4]+1]
for (g,d,b),den,energy,prod,lc,lb in itertools.product(grid,[1,1/.461],ec,ms,[100000,150000,200000],[300000,400000,500000]):
    v=[climate(s,g,d,b,den,energy,prod,lc,lb)[4] for s in ss]
    for s,x in zip(ss,v): add("nested_climate",s,"partial_GWP_t",x,v[1])
    reduction=100*(1-v[4]/v[1])
    if worst is None or reduction<worst[-1]: worst=[g,d,b,den,energy,prod,lc,lb,v[1],v[4],reduction]
    counts["gwp"][0]+=1;counts["gwp"][1]+=int(v[5]<v[4]<v[3]<v[2]<v[1]<v[0])
for (g,d,b),den,c,k in itertools.product(grid,[1,1/.461],pc,pol):
    v=[road(s,g,d,b,den,k,c) for s in ss]
    for s,x in zip(ss,v): add("nested_exhaust",s,k,x,v[1])
    if k in ("NOx","PM2_5"):
        a=counts["nox" if k=="NOx" else "pm"];a[0]+=1;a[1]+=int(v[2]<v[3]);a[2]+=int(v[3]<v[2])
assert len(base)==162 and len(diag)==18 and len(stats)==36
assert counts["gwp"][0]==len(grid)*2*len(ec)*len(ms)*9
for r in base: assert math.isclose(sum(r[4:8]),r[8],abs_tol=1e-7)
write("R9_7F_TRANSFER_GRID.csv","g_ownership,m_mileage,b_bus_supply,scenario,private_WTW_t,bus_WTW_t,private_production_t,bus_production_t,partial_GWP_t,reduction_vs_paired_S0_pct,CO_t,VOCs_t,NOx_t,PM2_5_t,PM10_t",base)
write("R9_7F_JINHUA_RETROSPECTIVE_DIAGNOSTIC.csv","g_ownership,m_mileage,b_bus_supply,scenario,private_WTW_t,bus_WTW_t,private_production_t,bus_production_t,partial_GWP_t,reduction_vs_paired_S0_pct,CO_t,VOCs_t,NOx_t,PM2_5_t,PM10_t",diag)
write("R9_7F_NESTED_ENVELOPE.csv","layer,scenario,indicator,min_annual,max_annual,min_reduction_pct,max_reduction_pct,paired_sets",[[*k,*v] for k,v in stats.items()])
write("R9_7F_REVERSAL_WITNESS.csv","g_ownership,m_mileage,b_bus_supply,mileage_denominator_multiplier,energy_case,production_set,car_lifetime_km,bus_lifetime_km,S0_partial_GWP_t,S3_partial_GWP_t,S3_reduction_pct",[worst])
write("R9_7F_ORDERING_COUNTS.csv","indicator,sets,preferred_or_strict_order_count,opposite_count",[["partial_GWP",counts["gwp"][0],counts["gwp"][1],counts["gwp"][0]-counts["gwp"][1]],["NOx",*counts["nox"]],["PM2_5",*counts["pm"]]])
print("PASS",counts)
