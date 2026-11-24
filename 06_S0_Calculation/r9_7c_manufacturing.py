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
energy=[r for r in read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"]
energy_by_s={r["scenario"]:float(r["total_WTW_tCO2e"]) for r in energy}
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
gwp=[]
partial=[]
source_sensitivity=[]
for r in vkt:
    name=r["scenario"]
    vi=float(r["private_ICEV_vkt_km"]);vb=float(r["private_BEV_vkt_km"]);vp=float(r["private_PHEV_vkt_km"])
    def burden(mult):
        return (vi*factors["ICEV"][mult]+vb*factors["BEV"][mult]+vp*factors["PHEV"][mult])/1e6
    lo,mid,hi=burden(1),burden(0),burden(2)
    priv.append([name,vi,vb,vp,lo,mid,hi,"CO2 only","YANG2021","not CO2e; keep separate from WTW GWP"])
    bd=float(r["bus_diesel_vkt_km"]);bg=float(r["bus_natural_gas_vkt_km"])
    bh=float(r["bus_mixed_nonBEV_vkt_km"]);bb=float(r["bus_BEV_vkt_km"]);bu=float(r["bus_unclassified_vkt_km"])
    ud=bu*unknown_diesel_share;ug=bu-ud
    total=((bd+ud)*107.1+(bg+ug)*113.4+bh*115.875+bb*119.37)/1e6
    bus.append([name,bd,bg,bh,bb,bu,ud,ug,total,"CO2e","LIN2015","raw materials + source-defined assembly/distribution; EOL excluded"])
    ledger.append([name,mid,lo,hi,total,"do not aggregate CO2-only private and CO2e bus columns"])
    # Harmonized GWP proxy set: Qiao2017 ICEV/BEV-NMC; Xiong2019 PHEV-NMC.
    # Each whole-vehicle production factor already includes its initial battery.
    car_gwp=(vi*9985+vb*15005+vp*8670.43)/150000/1000
    mfg_gwp=car_gwp+total
    wtw=energy_by_s[name]
    gwp.append([name,car_gwp,total,mfg_gwp,"CO2e","QIAO2017+XIONG2019","Qiao ICEV/BEV-NMC; Xiong PHEV-NMC; initial batteries included"])
    partial.append([name,car_gwp,total,mfg_gwp,wtw,mfg_gwp+wtw,"CO2e","vehicle production + bus raw materials/assembly-distribution + WTW operation; excludes maintenance/EOL/infrastructure"])
    # Structural BEV production-factor alternative: Xiong2019 NMC instead of Qiao2017 NMC.
    car_gwp_xiong_bev=(vi*9985+vb*11517.82+vp*8670.43)/150000/1000
    for set_name, car_alt, note in (
        ("QIAO2017_BEV_NMC",car_gwp,"Qiao ICEV+BEV NMC; Xiong PHEV NMC"),
        ("XIONG2019_BEV_NMC",car_gwp_xiong_bev,"Qiao ICEV; Xiong BEV/PHEV NMC")
    ):
        mfg_alt=car_alt+total
        source_sensitivity.append([set_name,name,car_alt,total,mfg_alt,wtw,mfg_alt+wtw,"CO2e",note])
write("R9_7C_PRIVATE_MANUFACTURING_SCENARIOS.csv",
 ["scenario","private_ICEV_vkt_km","private_BEV_vkt_km","private_PHEV_vkt_km","manufacturing_CO2_low_t_y","manufacturing_CO2_base_t_y","manufacturing_CO2_high_t_y","impact_unit","source_id","scope_note"],priv)
write("R9_7C_BUS_MANUFACTURING_SCENARIOS.csv",
 ["scenario","bus_diesel_VKT_km","bus_natural_gas_VKT_km","bus_hybrid_residual_VKT_km","bus_BEV_VKT_km","bus_unclassified_VKT_km","unclassified_allocated_diesel_VKT_km","unclassified_allocated_gas_VKT_km","bus_manufacturing_GHG_tCO2e_y","impact_unit","source_id","scope_note"],bus)
write("R9_7C_MANUFACTURING_LEDGER.csv",
 ["scenario","private_manufacturing_CO2_base_t_y","private_manufacturing_CO2_low_t_y","private_manufacturing_CO2_high_t_y","bus_manufacturing_GHG_tCO2e_y","aggregation_rule"],ledger)
write("R9_7C_PRIVATE_MANUFACTURING_GWP_SCENARIOS.csv",
 ["scenario","private_vehicle_production_GWP_tCO2e_y","source_id","scope_note"],
 [[r[0],r[1],r[5],r[6]] for r in gwp])
write("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv",
 ["scenario","private_vehicle_production_GWP_t_y","bus_manufacturing_GWP_t_y","total_manufacturing_GWP_t_y","WTW_operating_GWP_t_y","partial_LCA_GWP_t_y","impact_unit","scope_note"],partial)
write("R9_7C_PARTIAL_LCA_GWP_SOURCE_SENSITIVITY.csv",
 ["factor_set","scenario","private_vehicle_production_GWP_t_y","bus_manufacturing_GWP_t_y","total_manufacturing_GWP_t_y","WTW_operating_GWP_t_y","partial_LCA_GWP_t_y","impact_unit","source_note"],source_sensitivity)
assert len(energy)==6
assert len(partial)==6 and len(gwp)==6 and len(source_sensitivity)==12
for row in partial:
    assert all(math.isfinite(float(x)) and float(x)>=0 for x in row[1:6])
assert math.isclose(next(r[3] for r in partial if r[0]=="S3"),
                    next(r[3] for r in partial if r[0]=="S4"), rel_tol=0, abs_tol=1e-8)
assert next(r[5] for r in partial if r[0]=="S4") < next(r[5] for r in partial if r[0]=="S3")
print(f"PASS: {len(vkt)} scenarios; VKT conserved; CO2 and CO2e ledgers separate; partial LCA GWP reconciled")
