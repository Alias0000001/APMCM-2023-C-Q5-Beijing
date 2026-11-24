"""R9.7C: annualized vehicle-production burdens from pre-contest literature.
Keeps private-car CO2 and bus CO2e in separate ledgers; no invalid grand total.
"""
import csv, math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(name):
    with (D/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def write(name,header,rows):
    with (D/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(header);w.writerows(rows)
vkt=read("R9_7A_SIX_SCENARIO_VKT.csv")
unknown_diesel_share=1495/(1495+6795)
# Yang et al. (2021), source reports production-stage CO2, not CO2e.
# ICEV intensity is inferred from BEV/ICEV=1.33 and PHEV/ICEV=1.19.
ice=(92/1.33+82/1.19)/2
factors={
 "ICEV":(ice, (74/1.19), (90/1.19)),
 "BEV":(92,81,103),
 "PHEV":(82,74,90),
}
priv=[]
bus=[]
ledger=[]
for r in vkt:
    name=r["scenario"]
    vi=float(r["private_ICEV_VKT_km"]);vb=float(r["private_BEV_VKT_km"]);vp=float(r["private_PHEV_VKT_km"])
    def burden(mult):
        return (vi*factors["ICEV"][mult]+vb*factors["BEV"][mult]+vp*factors["PHEV"][mult])/1e6
    lo,mid,hi=burden(1),burden(0),burden(2)
    priv.append([name,vi,vb,vp,lo,mid,hi,"CO2 only","YANG2021","not CO2e; keep separate from WTW GWP"])
    bd=float(r["bus_diesel_vkt_km"]);bg=float(r["bus_natural_gas_vkt_km"])
    bh=float(r["bus_mixed_nonBEV_vkt_km"]);bb=float(r["bus_BEV_vkt_km"]);bu=float(r["bus_unclassified_vkt_km"])
    ud=bu*unknown_diesel_share;ug=bu-ud
    total=((bd+ud)*107.1+(bg+ug)*113.4+bh*115.875+bb*119.37)/1e6
    bus.append([name,bd,bg,bh,bb,bu,ud,ug,total,"CO2e","LIN2015","raw materials+assembly; EOL excluded"])
    ledger.append([name,mid,lo,hi,total,"do not sum CO2-only private and CO2e bus columns"])
write("R9_7C_PRIVATE_MANUFACTURING_SCENARIOS.csv",
 ["scenario","private_ICEV_VKT_km","private_BEV_VKT_km","private_PHEV_VKT_km","manufacturing_CO2_low_t_y","manufacturing_CO2_base_t_y","manufacturing_CO2_high_t_y","impact_unit","source_id","scope_note"],priv)
write("R9_7C_BUS_MANUFACTURING_SCENARIOS.csv",
 ["scenario","bus_diesel_VKT_km","bus_natural_gas_VKT_km","bus_hybrid_residual_VKT_km","bus_BEV_VKT_km","bus_unclassified_VKT_km","unclassified_allocated_diesel_VKT_km","unclassified_allocated_gas_VKT_km","bus_manufacturing_GHG_tCO2e_y","impact_unit","source_id","scope_note"],bus)
write("R9_7C_MANUFACTURING_LEDGER.csv",
 ["scenario","private_manufacturing_CO2_base_t_y","private_manufacturing_CO2_low_t_y","private_manufacturing_CO2_high_t_y","bus_manufacturing_GHG_tCO2e_y","aggregation_rule"],ledger)
print(f"PASS: {len(vkt)} scenarios; private and bus VKT conserved; CO2/CO2e intentionally not aggregated")
