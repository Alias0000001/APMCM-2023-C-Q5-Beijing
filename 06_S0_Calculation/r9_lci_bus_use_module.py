#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.2 partial bus use-stage LCI, with R7 base and R5/P0 alternative.

Only diesel and assigned electric-drive activity are quantified. CNG/LNG,
mixed non-BEV, and unclassified bus flows remain NA.
"""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"02_Cleaned_Data"
OUT=ROOT/"07_LCA_LCIA"
SCALE=1_000_000/21_858_000
DIESEL_L100=35.0
GAS_KG100=30.0
BUS_KWH_KM=0.626
DIESEL_DENSITY=0.84
DIESEL_LHV=42.652
EF={
 "diesel":{"CO2":.0907,"VOC":.000120,"NOx":.000024,"PM2.5":.000001,"SO2":.000026},
 "electricity":{"CO2":.190798,"VOC":.000017,"NOx":.000104,"PM2.5":.000014,"SO2":.000113},
}
POLLUTANTS=("CO2","VOC","NOx","PM2.5","SO2")
def main():
    with (DATA/"R7_S0_CO2_scenarios.csv").open(encoding="utf-8-sig",newline="") as f:
        r=next(x for x in csv.DictReader(f) if x["scenario"]=="S0_screening")
    num=lambda k:float(r[k])
    diesel_vkt=num("bus_diesel_vkt_km")
    diesel_l=diesel_vkt*DIESEL_L100/100
    diesel_mj=diesel_l*DIESEL_DENSITY*DIESEL_LHV
    base_bev_vkt=num("bus_bev_vkt_km_assumed")
    base_elec_kwh=base_bev_vkt*BUS_KWH_KM
    alt_n=16615
    alt_vkt=alt_n*45249.6*SCALE
    alt_elec=alt_n*28335.6*SCALE
    gas_kg=num("bus_gas_vkt_km")*GAS_KG100/100
    rows=[]
    def add(scenario,carrier,amount,unit,mj,status,note):
        result=dict(scenario=scenario,carrier=carrier,annual_amount=amount,unit=unit,
                    annual_energy_MJ=mj if mj is not None else "NA",
                    evidence_grade="D" if "R7" in note else "C",
                    status=status,note=note)
        for p in POLLUTANTS:
            result[p+"_kg_per_year"]="NA" if mj is None or carrier not in EF else mj*EF[carrier][p]
        rows.append(result)
    for scenario,elec_kwh,evkt in [("R7_base_q0.8",base_elec_kwh,base_bev_vkt),
                                   ("P0_alternative_nonH2_NEv",alt_elec,alt_vkt)]:
        add(scenario,"diesel",diesel_l,"L/year",diesel_mj,"modelled_R7_flow","R7 diesel VKT × assumed 35 L/100km")
        add(scenario,"electricity",elec_kwh,"kWh/year",elec_kwh*3.6,"modelled_or_alternative","R7 q=0.8" if scenario=="R7_base_q0.8" else "P0 annualized 2023-10 sample; replace base, do not add")
        add(scenario,"CNG_or_LNG",gas_kg,"kg/year",None,"NA_energy_and_WTW","CNG/LNG split and gas LHV unresolved")
        add(scenario,"mixed_nonBEV_unallocated","NA","NA",None,"NA_energy_and_WTW","No fuel type assigned; R7 placeholder CO2/km excluded")
        add(scenario,"unclassified_bus","NA","NA",None,"NA_energy_and_WTW","Powertrain and fuel unknown")
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/"R9_LCI_BUS_USE_STAGE.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print("R9 bus use-stage LCI written; CNG/LNG and unallocated mixed group remain NA.")
if __name__=="__main__":main()
