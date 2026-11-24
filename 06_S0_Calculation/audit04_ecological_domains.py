"""Audit-04: independent supplemental domains; never modify main baseline."""
import csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]; D=R/"02_Cleaned_Data"; L=R/"07_LCA_LCIA"
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,quoting=csv.QUOTE_ALL,lineterminator="\n");w.writerow(h);w.writerows(rows)
a=read(D/"R9_7A_SIX_SCENARIO_VKT.csv");z={r["scenario"]:r for r in read(D/"R9_7E_ENVIRONMENTAL_MATRIX.csv")}
f=read(L/"R9_3_NCM622_LCIA_FACTORS.csv")
F={(r["factor_case"],r["vehicle"],r["pollutant"]):float(r["sum_g_per_km"]) for r in read(D/"R9_7AUDIT04_WEAR_FACTORS.csv")}
wear=[]
for cs,ef,mul in [["EEA_equal","EEA_generic",1],["light_low","light_low",1],["light_high","light_high",1],["heavy_low","heavy_low",1],["heavy_high","heavy_high",1],["bus_low","EEA_generic",0.7],["bus_high","EEA_generic",1.3]]:
    for pol in ("PM2_5","PM10"):
        rr=[]
        for r in a:
            s=r["scenario"];c=F["EEA_generic","car",pol];b=F["EEA_generic","bus",pol];be=c if ef=="EEA_generic" else F[ef,"car_BEV",pol]
            pc=((float(r["private_ICEV_vkt_km"])+float(r["private_PHEV_vkt_km"]))*c+float(r["private_BEV_vkt_km"])*be)/1e6
            pb=((float(r["bus_total_vkt_km"])-float(r["bus_BEV_vkt_km"]))*b+float(r["bus_BEV_vkt_km"])*b*mul)/1e6
            tail=float(z[s]["road_"+pol+"_t_y"]);rr.append([cs,s,pol,pc,pb,tail,pc+pb+tail])
        base=next(r[6] for r in rr if r[1]=="S0")
        wear.extend(r+[100*(1-r[6]/base),"NA","wear and combustion only; dust resuspension and secondary PM excluded"] for r in rr)
caps=[];bat=[]
for r in a:
    s=r["scenario"];b=float(r["private_BEV_vkt_km"])/150000*40;p=float(r["private_PHEV_vkt_km"])/150000*12.8;t=b+p;caps.append([s,b,p,t])
    for x in f:
        for k,v in (("no_credit",float(x["material_stage_per_kWh"])+float(x["production_stage_per_kWh"])),("source_100pct_recycling",float(x["source_reported_total_per_kWh"]))):
            bat.append([s,k,x["indicator_id"],x["unit"]+"/year",b*v,p*v,t*v,v,t,"private hypothetical NCM622 only; not additive to main GWP"])
repl=[]
for cs,n in (("no_extra_pack",0),("half_extra_pack",.5),("one_extra_pack",1)):
    rr=[]
    for s,b,p,t in caps:
        extra=t*n*124.48/1e6;rr.append([cs,s,n,124.48,extra,float(z[s]["partial_GWP_kt_y"])+extra])
    base=next(r[5] for r in rr if r[1]=="S0")
    repl.extend(r+[100*(1-r[5]/base),"extra private pack only; bus replacement NA"] for r in rr)
write("R9_7AUDIT04_WEAR_SCENARIOS.csv",["case","scenario","pollutant","private_wear_t_y","bus_wear_t_y","combustion_t_y","covered_road_PM_t_y","paired_reduction_pct","resuspended_dust","scope"],wear)
write("R9_7AUDIT04_BATTERY_CAPACITY.csv",["scenario","BEV_capacity_kWh_y","PHEV_capacity_kWh_y","total_capacity_kWh_y"],caps)
write("R9_7AUDIT04_BATTERY_RECIPE.csv",["scenario","recycling_case","indicator","unit","private_BEV_amount","private_PHEV_amount","total_private_battery_amount","factor_per_kWh","annual_equivalent_capacity_kWh","scope"],bat)
write("R9_7AUDIT04_REPLACEMENT_STRESS.csv",["case","scenario","extra_pack_equiv","factor_kgCO2e_per_kWh","additional_GWP_kt","expanded_partial_GWP_kt","paired_reduction_pct","scope"],repl)
print("Audit04:",len(wear),len(bat),len(repl))
