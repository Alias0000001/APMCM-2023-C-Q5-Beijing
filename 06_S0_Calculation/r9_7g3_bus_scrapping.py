"""Historical bus scrapping only; independent optional expansion, no claim of full LCA."""
import csv
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h.split(","));w.writerows([[f"{x:.9f}" if isinstance(x,(int,float)) else x for x in r] for r in rows])
# Lin2015 Fig2 vehicle scrapping (kg CO2e per 1000 PKM) and Table5 load
src=[("diesel_bus",.04,42.5),("natural_gas_bus",.04,40.5),("diesel_hybrid_bus",.06,37.5),("battery_electric_bus",.17,34.5)]
fac=[[k,f,o,400000,f*o*400000/1e6,f*o,"Lin2015_Fig2_Table5","historical scrapping proxy; not complete recycling inventory"] for k,f,o in src]
b=read("R9_7C_BUS_MANUFACTURING_SCENARIOS.csv");m={r["scenario"]:r for r in read("R9_7E_ENVIRONMENTAL_MATRIX.csv")}
out=[]
for r in b:
    s=r["scenario"]
    v=[float(r["bus_diesel_VKT_km"])+float(r["unclassified_allocated_diesel_VKT_km"]),float(r["bus_natural_gas_VKT_km"])+float(r["unclassified_allocated_gas_VKT_km"]),float(r["bus_hybrid_residual_VKT_km"]),float(r["bus_BEV_VKT_km"])]
    e=sum(x*f[5]/1e6 for x,f in zip(v,fac));p=float(m[s]["partial_GWP_kt_y"])*1000;out.append([s,e,p,p+e])
z=next(r[3] for r in out if r[0]=="S0")
write("R9_7G3_BUS_SCRAPPING_FACTORS.csv","technology,source_scrapping_kgCO2e_per_1000_PKM,effective_passengers,lifetime_km,scrapping_tCO2e_per_bus,scrapping_gCO2e_per_vehicle_km,source,scope",fac)
write("R9_7G3_BUS_SCRAPPING_SENSITIVITY.csv","scenario,bus_scrapping_tCO2e_y,original_partial_GWP_tCO2e_y,expanded_partial_GWP_tCO2e_y,reduction_vs_paired_S0_pct,scope",[r+[100*(1-r[3]/z),"bus scrapping only; other unquantified stages remain NA"] for r in out])
print("PASS: independent bus scrapping expansion; original A-F results unchanged")
