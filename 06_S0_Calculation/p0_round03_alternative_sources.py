#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce round-3 substitute datasets for Beijing bus activity and local PHEV VKT."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02_Cleaned_Data"
OUT.mkdir(parents=True, exist_ok=True)

def write_csv(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)

bus_raw = [
    (2020, 23948, 1207, 28418, 106773, 182567),
    (2021, 23079, 1217, 28580, 113859, 229634),
    (2022, 23465, 1291, 30174, 98369, 172558),
    (2023, 23385, 1285, 29738, 115100, 208687),
    (2024, 21972, 1261, 29084, 109400, 209800),
    (2025, 20547, 1252, 28929, 97500, 188200),
]
rows = [[
    "year","operating_vehicles","operating_routes","route_length_km",
    "annual_VKT_10k_km","annual_VKT_km","annual_passenger_trips_10k",
    "annual_passenger_trips","mean_VKT_per_year_end_vehicle_km",
    "passenger_trips_per_vehicle_km","source_category","eligibility","notes"
]]
for y,n,l,length,v10,t10 in bus_raw:
    v, t = v10 * 10000, t10 * 10000
    eligibility = ("VKT_trips_pre_cutoff_confirmed_vehicle_count_publication_unverified" if y <= 2022
                   else "retrospective_full_year" if y == 2023
                   else "post_cutoff_trend_only")
    rows.append([y,n,l,length,v10,v,t10,t,round(v/n,3),round(t/v,6),
                 "公共电汽车",eligibility,
                 "2020-2022 VKT and trips are approximately cross-checked to 2023 MTN; vehicle-count and route fields have publication date unverified; category is not BEV-only"])
write_csv("P0_bus_activity_timeseries_2020_2025.csv", rows)

cost_rows = [
 ["period","VKT_km","passenger_trips","fuel_cost_10k_RMB",
  "electric_traction_cost_10k_RMB","fuel_cost_RMB",
  "electric_traction_cost_RMB","fuel_cost_RMB_per_vehicle_km",
  "electric_traction_cost_RMB_per_vehicle_km","combined_cost_RMB_per_vehicle_km",
  "source_accounting_scope","evidence_status","limitations"],
]
for period,vkt,trips,fuel10k,elec10k,status in [
 ("2022_FY",983690000,1725580000,179238.23,52430.40,"official_financial_disclosure"),
 ("2023_H1",552000000,977000000,82072.54,29434.64,"official_financial_disclosure_pre_cutoff"),
]:
    fuel, elec = fuel10k*10000, elec10k*10000
    cost_rows.append([period,vkt,trips,fuel10k,elec10k,fuel,elec,
        round(fuel/vkt,6),round(elec/vkt,6),round((fuel+elec)/vkt,6),
        "公益性客运出行服务成本",status,
        "Accounting costs, not physical energy quantities; 电车电力 boundary not confirmed as BEV-only; not LCA emission factors"])
write_csv("P0_bus_operating_cost_crosscheck_2022_2023H1.csv", cost_rows)

phev_rows = [
 ["row_type","season","metric","value","unit","sample_vehicles",
  "effective_vehicle_days","total_distance_km","standard_deviation_km",
  "annual_active_days_scenario","annualized_VKT_km_per_vehicle",
  "evidence_status","limitations"],
 ["overall","all","mean_daily_VKT",47.1,"km/vehicle-effective-day",45,10372,488521,56.2,"","",
  "peer_reviewed_local_sample","Study published 2021-09-29; observation window not stated; not a 2023 observation"],
 ["overall","all","sample_distance_per_vehicle",round(488521/45,3),"km/vehicle_over_sample_window",45,10372,488521,56.2,"","",
  "derived_from_study_table","Window length not stated; do not label as annual VKT"],
 ["overall","all","effective_days_per_vehicle",round(10372/45,3),"vehicle-days/vehicle",45,10372,488521,56.2,"","",
  "derived_from_study_table","Average effective observation days; not confirmed as a full calendar year"],
]
for season, value in [("spring",44.9),("summer",55.3),("autumn",50.6),("winter",49.3)]:
    phev_rows.append(["seasonal",season,"mean_daily_VKT",value,
        "km/vehicle-effective-day",45,10372,488521,56.2,"","",
        "peer_reviewed_local_sample","Seasonal sample statistic; not annualized"])
for days in (250,300,365):
    phev_rows.append(["annualization_scenario","all","annualized_VKT_from_47.1_daily",47.1,
        "km/vehicle-effective-day",45,10372,488521,56.2,days,round(47.1*days,1),
        "scenario_not_observation",f"Assumes {days} active driving days/year; sensitivity only"])
write_csv("P0_BJ_PHEV_daily_VKT_sensitivity.csv", phev_rows)
print("Round 3 substitute datasets written: bus activity, bus operating cost, Beijing PHEV daily VKT.")
