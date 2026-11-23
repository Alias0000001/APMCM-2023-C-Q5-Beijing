#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce P0 private passenger VKT and public-bus propulsion estimates.

Run from repository root:
    python 06_S0_Calculation/p0_vkt_propulsion_scenarios.py

Only standard-library modules are used. The script writes derived analysis
tables; it never changes raw source records.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02_Cleaned_Data"
OUT.mkdir(parents=True, exist_ok=True)

# Beijing 2023 official stock counts (vehicles)
POP = 21_858_000
TARGET_POP = 1_000_000
PRIVATE_PASSENGER = 5_073_000
PRIVATE_NEV = 528_000
PRIVATE_NON_NEV = PRIVATE_PASSENGER - PRIVATE_NEV
SCALE = TARGET_POP / POP

# Private passenger VKT inputs
# 2023 private-car daily intensity reported in the 2024 China Major Cities
# Charging Infrastructure Monitoring Report; annualized over 365 days.
D_ALL_PRIVATE = 28.4 * 365.0
# 2023-10 private BEV: 9.2 charging sessions/month × 169.6 km/session.
# Annualized by ×12; this is a one-month extrapolation, not an observed
# full-year odometer mean.
D_BEV_2023 = 9.2 * 169.6 * 12.0
# 2022 comparator: 8 charging sessions/month × 129 km/session × 12.
D_BEV_2022 = 8.0 * 129.0 * 12.0
# Shanghai 2018 private-PHEV GPS sample mean annual-window distance.
D_PHEV_MEAN = 14_774.95
D_PHEV_Q1 = 7_333.0
D_PHEV_MEDIAN = 12_648.0
D_PHEV_Q3 = 19_373.0
# National 2023 NEV stock: 76.04% BEV; remaining 23.96% is PHEV + fuel cell.
# For Beijing private passenger NEVs, the non-BEV share is treated as PHEV
# for scenario modelling; this is a proxy, not a local cross-tab.
PHEV_SHARES = [0.10, 0.2396, 0.30]

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def private_scenarios() -> list[dict]:
    rows = []
    total_vkt = PRIVATE_PASSENGER * D_ALL_PRIVATE
    for p_phev in PHEV_SHARES:
        n_phev = PRIVATE_NEV * p_phev
        n_bev = PRIVATE_NEV - n_phev
        n_ice = PRIVATE_NON_NEV
        # Estimate the non-NEV/ICE annual VKT as the residual that reconciles
        # class-specific BEV/PHEV estimates to the city-wide private-car
        # activity anchor. This is a model-derived value, not an observed
        # ICE-only annual mileage.
        d_ice = (
            total_vkt - n_bev * D_BEV_2023 - n_phev * D_PHEV_MEAN
        ) / n_ice
        counts = {"ICE_or_nonNEV": n_ice, "BEV": n_bev, "PHEV": n_phev}
        distances = {"ICE_or_nonNEV": d_ice, "BEV": D_BEV_2023, "PHEV": D_PHEV_MEAN}
        vkts = {k: counts[k] * distances[k] for k in counts}
        total = sum(vkts.values())
        for k in counts:
            rows.append({
                "scenario": f"PHEV_share_{p_phev:.4f}",
                "propulsion_group": k,
                "share_of_private_NEV_assumed_PHEV": f"{p_phev:.4f}",
                "fleet_count_Beijing_2023": f"{counts[k]:.3f}",
                "annual_VKT_per_vehicle_km": f"{distances[k]:.3f}",
                "annual_total_VKT_Beijing_km": f"{vkts[k]:.3f}",
                "vehicle_stock_share": f"{counts[k] / PRIVATE_PASSENGER:.8f}",
                "VKT_share": f"{vkts[k] / total:.8f}",
                "scaled_count_1m_city": f"{counts[k] * SCALE:.6f}",
                "scaled_annual_VKT_1m_city_km": f"{vkts[k] * SCALE:.3f}",
                "total_private_VKT_Beijing_km": f"{total:.3f}",
                "total_private_VKT_1m_city_km": f"{total * SCALE:.3f}",
                "population_scale_factor": f"{SCALE:.12f}",
                "evidence_status": "derived_scenario_not_direct_observation",
            })
    return rows

def bus_estimates() -> list[dict]:
    total_bus = 23_385
    total_bus_vkt = 1_151_000_000.0
    new_energy_bus = 16_832
    hydrogen_bus = 217
    clean_plus_new_share = 0.947
    # Rounded estimate from the reported combined clean-energy + new-energy
    # share; CNG/LNG split remains unavailable.
    clean_plus_new_count = round(total_bus * clean_plus_new_share)
    clean_energy_count = clean_plus_new_count - new_energy_bus
    other_count = total_bus - clean_plus_new_count
    bev_est = new_energy_bus - hydrogen_bus

    bev_monthly_km = 3_770.8
    bev_monthly_kwh = 2_361.3
    bev_km_year = bev_monthly_km * 12.0
    bev_kwh_year = bev_monthly_kwh * 12.0
    bev_vkt = bev_est * bev_km_year
    residual_vkt = total_bus_vkt - bev_vkt

    rows = [
        {
            "metric": "total_public_bus_category_operating_vehicles",
            "value": total_bus, "unit": "vehicles", "evidence_status": "official_observation",
            "calculation_or_note": "2023 Beijing Public Transport Group historical table; source label 公共电汽车",
        },
        {
            "metric": "new_energy_buses",
            "value": new_energy_bus, "unit": "vehicles", "evidence_status": "official_operator_report",
            "calculation_or_note": "2023 social responsibility report; NEV category, not BEV-only",
        },
        {
            "metric": "hydrogen_fuel_cell_buses",
            "value": hydrogen_bus, "unit": "vehicles", "evidence_status": "official_snapshot_2023_06_19",
            "calculation_or_note": "2023 municipal reply; 5 legacy + 212 Winter Olympics buses; snapshot date is 7 Dec",
        },
        {
            "metric": "non_hydrogen_new_energy_bus_estimate",
            "value": bev_est, "unit": "vehicles", "evidence_status": "derived_proxy",
            "calculation_or_note": "16,832 NEV minus 217 hydrogen; interpreted as BEV/electric-drive proxy pending exact year-end cross-tab",
        },
        {
            "metric": "clean_energy_bus_estimate",
            "value": clean_energy_count, "unit": "vehicles", "evidence_status": "derived_rounded_aggregate",
            "calculation_or_note": "round(23,385 × 94.7%) minus 16,832; likely CNG/LNG aggregate; exact split unavailable",
        },
        {
            "metric": "other_bus_estimate",
            "value": other_count, "unit": "vehicles", "evidence_status": "derived_rounded_residual",
            "calculation_or_note": "23,385 minus rounded clean-energy + new-energy total; could include diesel/hybrid/trolley/other",
        },
        {
            "metric": "clean_energy_plus_new_energy_share",
            "value": clean_plus_new_share, "unit": "share", "evidence_status": "official_operator_report",
            "calculation_or_note": "2023 social responsibility report; do not interpret as pure-electric share",
        },
        {
            "metric": "total_public_bus_category_annual_VKT",
            "value": total_bus_vkt, "unit": "vehicle-km/year", "evidence_status": "official_operator_statistics",
            "calculation_or_note": "2023 historical table; not propulsion-specific",
        },
        {
            "metric": "BEV_bus_average_monthly_VKT",
            "value": bev_monthly_km, "unit": "vehicle-km/month", "evidence_status": "literature_big_data_month_2023_10",
            "calculation_or_note": "2023-10 electric-bus sample mean from Beijing EV charging report",
        },
        {
            "metric": "BEV_bus_annualized_VKT_per_vehicle",
            "value": bev_km_year, "unit": "vehicle-km/vehicle/year", "evidence_status": "derived_annualization",
            "calculation_or_note": "3,770.8 × 12; one-month annualization, not a full-year odometer observation",
        },
        {
            "metric": "BEV_bus_estimated_annual_total_VKT",
            "value": bev_vkt, "unit": "vehicle-km/year", "evidence_status": "derived_estimate",
            "calculation_or_note": "estimated BEV/electric-drive count × annualized monthly mean VKT",
        },
        {
            "metric": "BEV_bus_estimated_share_of_total_bus_VKT",
            "value": bev_vkt / total_bus_vkt, "unit": "share", "evidence_status": "derived_estimate",
            "calculation_or_note": "BEV estimated VKT divided by total public-bus category VKT",
        },
        {
            "metric": "non_BEV_unallocated_bus_VKT_residual",
            "value": residual_vkt, "unit": "vehicle-km/year", "evidence_status": "derived_residual_not_fuel_split",
            "calculation_or_note": "total bus VKT minus estimated BEV VKT; not split among hydrogen/CNG/LNG/diesel/hybrid/trolley",
        },
        {
            "metric": "BEV_bus_average_monthly_electricity",
            "value": bev_monthly_kwh, "unit": "kWh/vehicle/month", "evidence_status": "literature_big_data_month_2023_10",
            "calculation_or_note": "2023-10 electric-bus sample mean",
        },
        {
            "metric": "BEV_bus_annualized_electricity_per_vehicle",
            "value": bev_kwh_year, "unit": "kWh/vehicle/year", "evidence_status": "derived_annualization",
            "calculation_or_note": "2,361.3 × 12",
        },
        {
            "metric": "BEV_bus_estimated_annual_total_electricity",
            "value": bev_est * bev_kwh_year, "unit": "kWh/year", "evidence_status": "derived_estimate",
            "calculation_or_note": "estimated BEV/electric-drive count × annualized monthly electricity per vehicle",
        },
        {
            "metric": "BEV_bus_electricity_intensity",
            "value": 62.6, "unit": "kWh/100km", "evidence_status": "literature_big_data_2023",
            "calculation_or_note": "2023 Beijing electric-bus actual electricity consumption intensity",
        },
    ]
    for row in rows:
        row["scaled_value_1m_city"] = (
            f"{float(row['value']) * SCALE:.6f}"
            if row["unit"] in {"vehicles", "vehicle-km/year"} else ""
        )
        row["population_scale_factor"] = f"{SCALE:.12f}"
    return rows

def main() -> None:
    private = private_scenarios()
    bus = bus_estimates()
    write_csv(OUT / "P0_private_VKT_propulsion_scenarios.csv", private)
    write_csv(OUT / "P0_bus_propulsion_VKT_estimates.csv", bus)
    print(f"Population scaling factor: {SCALE:.12f}")
    print(f"Private-car scenarios written: {len(private)} rows")
    print(f"Bus propulsion/VKT estimates written: {len(bus)} rows")
    print("All class-specific results are labelled as derived/proxy where applicable.")

if __name__ == "__main__":
    main()
