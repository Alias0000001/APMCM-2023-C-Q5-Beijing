"""Boundary correction and source-set substitution, no modification to archival input tables."""
import csv
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(n,h,rows):
    with (D/n).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(h);w.writerows(rows)
sources={r["source_id"]:float(r["value"]) for r in read("R9_7FIX_SOURCE_BOUNDARY.csv")}
m=read("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv")
q=next(r for r in m if r["source_id"]=="QIAO17_ICE")
L=float(q["lifetime_km"]);phev=next(r for r in m if r["source_id"]=="XIONG19_PHEV_NMC");ph=float(phev["factor_value"])*1000/L
V=read("R9_7A_SIX_SCENARIO_VKT.csv");G={r["scenario"]:r for r in read("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")}
out=[]
for name,ice,bev,scope in [
 ("Qiao_NMC_reference",sources["QIAO17_ICE"]/L,sources["QIAO17_BEV_NMC"]/L,"Qiao CTG source-specific with consumable replacements"),
 ("Qiao_LFP_same_study",sources["QIAO17_ICE"]/L,sources["QIAO17_BEV_LFP"]/L,"same-study BEV chemistry alternative; PHEV unchanged"),
 ("Gan_BEV100_vehicle_cycle",sources["GAN23_ICE"]/1000,sources["GAN23_BEV100"]/1000,"replace entire private ICEV/BEV production with Gan vehicle cycle; PHEV/bus unmatched"),
 ("Gan_BEV300_vehicle_cycle",sources["GAN23_ICE"]/1000,sources["GAN23_BEV300"]/1000,"replace entire private ICEV/BEV production with Gan vehicle cycle; PHEV/bus unmatched")]:
    tmp=[]
    for r in V:
        s=r["scenario"];c=(float(r["private_ICEV_vkt_km"])*ice+float(r["private_BEV_vkt_km"])*bev+float(r["private_PHEV_vkt_km"])*ph)/1000
        b=float(G[s]["bus_manufacturing_GWP_t_y"]);w=float(G[s]["WTW_operating_GWP_t_y"])
        total=(c+b+w)/1000
        if name=="Qiao_NMC_reference":assert abs(total-float(G[s]["partial_LCA_GWP_t_y"])/1000)<1e-6
        tmp.append((s,c/1000,b/1000,w/1000,total))
    z=next(x[-1] for x in tmp if x[0]=="S0")
    out.extend([[name,*x,100*(1-x[-1]/z),scope] for x in tmp])
write("R9_7FIX_BOUNDARY_ALTERNATIVES.csv",["case","scenario","private_vehicle_cycle_or_production_kt","bus_production_kt","WTW_kt","included_GWP_kt","paired_reduction_pct","scope"],out)
C=read("R9_7AUDIT04_STAGE_COVERAGE.csv")
for r in C:
    if r["vehicle"] in ("private_ICEV","private_BEV") and r["stage"]=="maintenance":
        r.update(coverage="INCLUDED_PARTIAL_CONSUMABLES",boundary="selected tire/fluids/lead-acid replacement in Qiao aggregate; no additive maintenance; full maintenance unresolved",source="R9_7FIX_SOURCE_BOUNDARY.csv")
    if r["vehicle"]=="private_BEV" and r["stage"]=="replacement_traction_battery":
        r["boundary"]="additional private NMC pack design; Table 2 Qiao traction pack has no replacement count; not added to Gan vehicle cycle"
write("R9_7FIX_STAGE_COVERAGE.csv",list(C[0]),[list(r.values()) for r in C])
assert len(C)==128 and sum(r["coverage"]=="INCLUDED_PARTIAL_CONSUMABLES" for r in C)==2
print("PASS: source substitutions and corrected stage coverage")
