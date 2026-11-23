#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Policy-aware sensitivity for Beijing private BEV/PHEV VKT mix.

The national 76.04% BEV share is retained only as a comparator. Beijing's
new-energy small-passenger-car indicator is defined as pure-electric in the
local quota policy, while the 2023 statistical count's exact propulsion
cross-tab remains unavailable. Therefore no single BEV/PHEV split is asserted.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02_Cleaned_Data"
OUT.mkdir(parents=True, exist_ok=True)

POP = 21_858_000
TARGET_POP = 1_000_000
N_PRIVATE = 5_073_000
N_PRIVATE_NEV = 528_000
N_ICE_OR_NONNEV = N_PRIVATE - N_PRIVATE_NEV
SCALE = TARGET_POP / POP

# Retrospective 2023 activity anchors:
D_PRIVATE_ALL = 28.4 * 365.0
D_BEV = 9.2 * 169.6 * 12.0
# Historical local Beijing PHEV effective-day mean; active-day count is varied.
D_PHEV_EFFECTIVE_DAY = 47.1
PHEV_SHARES = [0.00, 0.05, 0.10, 0.2396]
PHEV_ACTIVE_DAYS = [250, 300, 365]

def write_csv(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def main():
    total_private_vkt = N_PRIVATE * D_PRIVATE_ALL
    rows = [[
        "scenario_id","assumed_PHEV_share_within_private_NEV",
        "assumed_PHEV_active_days_per_year","private_ICE_or_nonNEV_count",
        "private_BEV_count","private_PHEV_count",
        "annual_VKT_per_ICE_or_nonNEV_km","annual_VKT_per_BEV_km",
        "annual_VKT_per_PHEV_km","ICE_or_nonNEV_total_VKT_km",
        "BEV_total_VKT_km","PHEV_total_VKT_km","total_private_VKT_km",
        "ICE_or_nonNEV_VKT_share","BEV_VKT_share","PHEV_VKT_share",
        "scaled_private_vehicle_count_1m_city",
        "scaled_total_private_VKT_1m_city_km","scenario_basis","evidence_status"
    ]]
    for p_share in PHEV_SHARES:
        for active_days in PHEV_ACTIVE_DAYS:
            n_phev = N_PRIVATE_NEV * p_share
            n_bev = N_PRIVATE_NEV - n_phev
            d_phev = D_PHEV_EFFECTIVE_DAY * active_days if n_phev > 0 else 0.0
            d_ice = (total_private_vkt - n_bev * D_BEV - n_phev * d_phev) / N_ICE_OR_NONNEV
            vkt_ice = N_ICE_OR_NONNEV * d_ice
            vkt_bev = n_bev * D_BEV
            vkt_phev = n_phev * d_phev
            if p_share == 0:
                basis = "boundary case if all 528000 reported private NEVs are BEV; not asserted as fact"
            elif p_share == 0.2396:
                basis = "national 2023 non-BEV mix comparator includes FCEV; all non-BEV treated as PHEV in this scenario; not Beijing central"
            else:
                basis = f"low local-mix sensitivity {p_share:.0%}; not observed"
            rows.append([
                f"PHEVshare_{p_share:.4f}_activeDays_{active_days}",
                p_share, active_days, N_ICE_OR_NONNEV, n_bev, n_phev,
                round(d_ice, 3), round(D_BEV, 3), round(d_phev, 3),
                round(vkt_ice, 3), round(vkt_bev, 3), round(vkt_phev, 3),
                round(total_private_vkt, 3), round(vkt_ice/total_private_vkt, 8),
                round(vkt_bev/total_private_vkt, 8), round(vkt_phev/total_private_vkt, 8),
                round(N_PRIVATE*SCALE, 6), round(total_private_vkt*SCALE, 3),
                basis, "scenario_not_observation"
            ])
    write_csv("P0_private_VKT_policy_mix_sensitivity.csv", rows)
    print("Wrote policy-aware private BEV/PHEV mix sensitivity grid (12 scenarios).")

if __name__ == "__main__":
    main()
