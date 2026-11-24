"""Conditional service sensitivity; actual PKM remains missing."""
import csv,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h.split(","));w.writerows([[f"{x:.9f}" if isinstance(x,(float,int)) else x for x in r] for r in rows])
a=read("R9_7A_SIX_SCENARIO_VKT.csv")
e={r["scenario"]:r for r in read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"}
m={r["scenario"]:r for r in read("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")}
p={r["parameter"]:float(r["value"]) for r in read("R9_7A_CONTEST_ACTIVITY_INPUTS.csv")}
V=float(a[0]["private_total_vkt_km"]);B=float(a[0]["bus_total_vkt_km"])
T=p["bus_boardings"]*p["target_population"]/p["reference_population"]
cases=[["short",5,1,1,1],["reference",10.9,1.24,1,1],["long",15,1.6,1,1],["BEV_lower",10.9,1.24,0.81,0.8],["BEV_higher",10.9,1.24,1.2,1.2]]
rows=[];mr=[]
def burdens(s):
    cg=float(e[s]["private_WTW_tCO2e"]);bg=float(e[s]["bus_WTW_tCO2e"])
    return cg,bg,cg+float(m[s]["private_vehicle_production_GWP_t_y"]),bg+float(m[s]["bus_manufacturing_GWP_t_y"])
for case,d,o,cr,br in cases:
    def occ(r): return o*(1+float(r["private_BEV_vkt_km"])/V*(cr-1)),T*d/B*(1+float(r["bus_BEV_vkt_km"])/B*(br-1))
    c0,b0=occ(next(r for r in a if r["scenario"]=="S0"))
    for r in a:
        s=r["scenario"];c,b=occ(r);cp,bp=V*c,B*b;cg,bg,ec,eb=burdens(s);fc,fb=c0/c,b0/b
        assert min(c,b)>=1 and math.isclose(V*fc*c,V*c0) and math.isclose(B*fb*b,B*b0)
        assert math.isclose(ec+eb,float(m[s]["partial_LCA_GWP_t_y"]),abs_tol=1e-5)
        rows.append([case,s,d,o,cr,br,c,b,cp,bp,cg*1e6/V,bg*1e6/B,ec*1e6/V,eb*1e6/B,cg*1e6/cp,bg*1e6/bp,ec*1e6/cp,eb*1e6/bp,V*fc,B*fb,cg*fc+bg*fb,ec*fc+eb*fb,ec+eb])
f=1/p["central_city_dispatch_rate"];d=p["private_daily_distance"]*365
for r in a:
    s=r["scenario"];cg,bg,ec,eb=burdens(s);mr.append([s,d/f,d,V,V*f,B,cg+bg,cg*f+bg,ec+eb,ec*f+eb])
assert len(rows)==30 and len(mr)==6
write("R9_7D_SERVICE_SENSITIVITY.csv","case,scenario,bus_trip_km_proxy,car_occupancy_proxy,car_BEV_occupancy_multiplier,bus_BEV_occupancy_multiplier,car_effective_pax,bus_effective_pax,car_PKM,bus_PKM,car_WTW_g_per_VKT,bus_WTW_g_per_VKT,car_partial_GWP_g_per_VKT,bus_partial_GWP_g_per_VKT,car_WTW_g_per_PKM,bus_WTW_g_per_PKM,car_partial_GWP_g_per_PKM,bus_partial_GWP_g_per_PKM,equal_service_car_VKT,equal_service_bus_VKT,equal_service_WTW_tCO2e,equal_service_partial_GWP_tCO2e,fixed_VKT_partial_GWP_tCO2e",rows)
write("R9_7D_MILEAGE_DENOMINATOR_SENSITIVITY.csv","scenario,base_km_per_car_year,alternative_km_per_car_year,base_car_VKT,alternative_car_VKT,bus_VKT_unchanged,base_WTW_tCO2e,alternative_WTW_tCO2e,base_partial_GWP_tCO2e,alternative_partial_GWP_tCO2e",mr)
print("PASS: 30 service cases and six mileage alternatives")
