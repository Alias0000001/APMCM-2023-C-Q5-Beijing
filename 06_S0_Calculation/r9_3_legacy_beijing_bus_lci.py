#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.3 legacy Beijing bus LCA transfer (2015 literature x 2023 R7 VKT).

The 2015 paper's specific 2011-era Beijing power mix and vehicle technologies
are NOT a 2023 Beijing observation. This does NOT overwrite the R7 baseline.
Original study: Lin et al. 2015, Acta Scientiae Circumstantiae 35(2), 576-584.
"""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"07_LCA_LCIA"
R7=ROOT/"02_Cleaned_Data"/"R7_S0_CO2_scenarios.csv"
ACTIVITY_KEY={
  "diesel_CDB":"bus_diesel_vkt_km",
  "natural_gas_NGB":"bus_gas_vkt_km",
  "battery_electric_BEB":"bus_bev_vkt_km_assumed",
  "diesel_hybrid_DHEB":None,
}
# 2015 paper Table 5 only. Never label as 2023 local occupancy.
EFFECTIVE_PASSENGERS_2015={
 "diesel_CDB":42.5,
 "natural_gas_NGB":40.5,
 "diesel_hybrid_DHEB":37.5,
 "battery_electric_BEB":34.5,
}
def load(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def main():
    r7=next(x for x in load(R7) if x["scenario"]=="S0_screening")
    factor_rows=load(D/"R9_3_BEIJING_2015_BUS_WTW_FACTORS.csv")
    material=load(D/"R9_3_BEIJING_2015_BUS_MATERIAL_SHARES.csv")
    result=[]
    check=[]
    for f in factor_rows:
        vehicle=f["bus_type"]
        k=ACTIVITY_KEY[vehicle]
        vkt=float(r7[k]) if k else None
        wtt=float(f["WTT_gCO2e_per_MJ"])
        ttw=float(f["TTW_gCO2e_per_MJ"])
        for ac in ("off","on"):
            intensity=float(f["ac_"+ac+"_MJ_per_vehicle_km"])
            wtt_kg_km=intensity*wtt/1000
            ttw_kg_km=intensity*ttw/1000
            result.append(dict(bus_type=vehicle,AC_mode_2015=ac,
              reference_year_of_activity=2023,
              legacy_factor_year=2015,
              assigned_annual_VKT_km=vkt if vkt is not None else "NA",
              MJ_per_vehicle_km_2015=intensity,
              WTT_kgCO2e_per_vehicle_km=wtt_kg_km,
              TTW_kgCO2e_per_vehicle_km=ttw_kg_km,
              WTW_kgCO2e_per_vehicle_km=wtt_kg_km+ttw_kg_km,
              WTW_annual_tCO2e=(vkt*(wtt_kg_km+ttw_kg_km)/1000 if vkt is not None else "NA"),
              effective_passengers_per_bus_2015=EFFECTIVE_PASSENGERS_2015[vehicle],
              optional_PKM_2015_occupancy_assumption=(vkt*EFFECTIVE_PASSENGERS_2015[vehicle]
                    if vkt is not None else "NA"),
              source_id="LIN2015_BEIJING_BUS",
              evidence_status="CROSS_YEAR_HISTORICAL_STRESS_NOT_2023_CALIBRATION",
              caveat="2015 technology/2011 power mix, 2023 assigned VKT; BEB q=0.8 from R7 hypothetical; hybrid VKT unknown; do not combine with R9 Yang2021 WTW"))
        check.append(dict(check=vehicle+"_material_shares_sum",computed=sum(
            float(r["share_vehicle_mass"]) for r in material if r["bus_type"]==vehicle),
            expected=1.0,pass_fail="INCOMPLETE_COMPONENT_COVERAGE_EXPECTED",
            note="Published shares exclude some components (especially BEB battery); no mass conversion without 2023 bus mass"))
    assert len(result)==8
    assert len(check)==4
    with (D/"R9_3_BEIJING_2015_BUS_TRANSFER_STRESS.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    with (D/"R9_3_BEIJING_2015_BUS_FRACTION_CHECK.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(check[0]));w.writeheader();w.writerows(check)
    print("R9.3 historical bus stress: 8 conditional rows, 4 incomplete shares checks. No 2023 bus manufacturing total.")
if __name__=="__main__":main()
