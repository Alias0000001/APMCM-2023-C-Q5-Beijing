#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R5: Public-source Beijing 2023 bus/VKT proxies and private-BEV correction.

Usage:
    python 06_S0_Calculation/r5_public_proxy_scenarios.py

Read 2023-Apr operator interview snapshot and 2023-Oct direct pure-BEV
monthly measurement. No downloaded source file is altered. Generated outputs
remain class-C scenarios, NOT source-authoritative 2023 fuel-specific VKT.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Cleaned_Data"
SNAPSHOT = DATA / "R5_bus_2023_04_fleet_snapshot.csv"
BEV = DATA / "R5_private_bev_2023_october_observed.csv"
PVT_OLD = DATA / "P0_private_VKT_policy_mix_sensitivity.csv"

BEIJING_POP = 21_858_000
TARGET_POP = 1_000_000
SCALE = TARGET_POP / BEIJING_POP
BUS_2023_ANNUAL_TOTAL_VKT = 1_151_000_000
PVT_2023_STOCK = 5_073_000
PVT_2023_NEV_STOCK = 528_000
PVT_DAILY_ACTIVITY = 28.4
PVT_ICE_STOCK = PVT_2023_STOCK - PVT_2023_NEV_STOCK
TARGET_PVT_TOTAL_VKT = PVT_2023_STOCK * PVT_DAILY_ACTIVITY * 365

def load(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def save(path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def bus():
    raw = load(SNAPSHOT)
    counts = {r["category"]: int(r["vehicles"]) for r in raw}
    assert sum(counts.values()) == 23_747
    assert counts["unclassified_difference"] == 6
    result = []
    for rel in (0.8, 1.0, 1.2):
        weighted = {
            k: v * (rel if k == "new_energy_electric_drive_mixed" else 1.0)
            for k, v in counts.items()
        }
        denom = sum(weighted.values())
        allocation = {
            k: BUS_2023_ANNUAL_TOTAL_VKT * w / denom for k, w in weighted.items()
        }
        assert abs(sum(allocation.values()) - BUS_2023_ANNUAL_TOTAL_VKT) < 1e-4
        for k in counts:
            result.append({
                "scenario": f"electric_drive_relative_VKT_{rel:.1f}",
                "propulsion_group": k,
                "April_2023_snapshot_count": counts[k],
                "relative_annual_VKT_per_vehicle_assumption":
                    rel if k == "new_energy_electric_drive_mixed" else 1.0,
                "group_annual_VKT_Beijing_km_estimate": f"{allocation[k]:.6f}",
                "group_VKT_share": f"{allocation[k]/BUS_2023_ANNUAL_TOTAL_VKT:.9f}",
                "scaled_group_VKT_one_million_city_km": f"{allocation[k]*SCALE:.6f}",
                "source_count_id": "BJ-BUS-ENERGY-MIX-2023APR",
                "source_VKT_id": "BJ-BUS-HIST",
                "evidence_status": "PROXY_not_observed_2023_fuel_specific_VKT",
                "caveat": "April fleet snapshot mixed with full-year VKT; electric-drive is not pure BEV; r is a stress assumption.",
            })
    save(DATA / "R5_bus_vkt_allocation_scenarios.csv", result)
    return len(result)

def private():
    observations = load(BEV)
    x = next(r for r in observations if r["observation_period"] == "2023-10")
    bev_annual = float(x["monthly_mean_distance_km"]) * 12
    assert abs(bev_annual - 18_619.2) < 1e-6
    old = load(PVT_OLD)
    result = []
    for r in old:
        phev_share = float(r["assumed_PHEV_share_within_private_NEV"])
        days = int(r["assumed_PHEV_active_days_per_year"])
        n_phev = PVT_2023_NEV_STOCK * phev_share
        n_bev = PVT_2023_NEV_STOCK - n_phev
        d_phev = 47.1 * days if n_phev else 0.0
        vkt_bev = n_bev * bev_annual
        vkt_phev = n_phev * d_phev
        vkt_ice = TARGET_PVT_TOTAL_VKT - vkt_bev - vkt_phev
        d_ice = vkt_ice / PVT_ICE_STOCK
        assert d_ice > 0
        assert abs(vkt_ice + vkt_bev + vkt_phev - TARGET_PVT_TOTAL_VKT) < 1e-4
        result.append({
            "scenario": f"phev_share_{phev_share:.4f}_active_days_{days}",
            "phev_share_within_NEV_assumed": phev_share,
            "PHEV_active_days_assumed": days,
            "BEV_count_assumed": f"{n_bev:.3f}",
            "PHEV_count_assumed": f"{n_phev:.3f}",
            "ICE_nonNEV_count": PVT_ICE_STOCK,
            "BEV_annual_VKT_per_vehicle_from_october_km": bev_annual,
            "PHEV_annual_VKT_per_vehicle_assumed_km": d_phev,
            "ICE_nonNEV_annual_VKT_per_vehicle_residual_km": f"{d_ice:.6f}",
            "BEV_annual_total_VKT_km": f"{vkt_bev:.3f}",
            "PHEV_annual_total_VKT_km": f"{vkt_phev:.3f}",
            "ICE_nonNEV_annual_total_VKT_km": f"{vkt_ice:.3f}",
            "private_total_annual_VKT_km": f"{TARGET_PVT_TOTAL_VKT:.3f}",
            "scaled_total_private_VKT_one_million_city_km": f"{TARGET_PVT_TOTAL_VKT*SCALE:.3f}",
            "evidence_status": "SENSITIVITY_NOT_2023_ANNUAL_ODOMETER_MEAN",
            "caveat": "Oct BEV monthly mean multiplied 12; ICE residual anchored to conditional 28.4km/day ×365; PHEV annual active days assumed.",
        })
    save(DATA / "R5_private_VKT_corrected_sensitivity.csv", result)
    return len(result)

if __name__ == "__main__":
    print("Bus rows:", bus())
    print("Private rows:", private())
    print("Observation year: 2023; publication year may be 2024/2025.")
