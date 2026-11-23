#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scale documented extensive Beijing 2023 indicators to a 1-million-person city.

This is a linear population-scaling baseline only. It does not estimate missing
private-car VKT, BEV/PHEV split, bus PKM, propulsion shares, or LCA factors.
Run from any working directory:
    python 06_S0_Calculation/scale_official_inputs.py
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 28
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "02_Cleaned_Data" / "beijing_2023_official_observations.csv"
OUTPUT = ROOT / "02_Cleaned_Data" / "beijing_2023_population_scaled_inputs.csv"
TARGET_POPULATION = Decimal("1000000")
POPULATION_ID = "BJ-P01"

# Extensive counts and annual totals only. Intensity factors are intentionally excluded.
SCALE_IDS = {
    "BJ-P02", "BJ-P03", "BJ-P04",
    "BJ-BUS01", "BJ-BUS02", "BJ-BUS03",
    "BJ-BUS04", "BJ-BUS05", "BJ-BUS06",
}

def main() -> None:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    by_id = {row["parameter_id"]: row for row in rows}
    if POPULATION_ID not in by_id:
        raise ValueError(f"Missing population denominator {POPULATION_ID}")

    base_population = Decimal(by_id[POPULATION_ID]["value"])
    if base_population <= 0:
        raise ValueError("Population denominator must be positive")
    factor = TARGET_POPULATION / base_population

    output_rows = []
    for row in rows:
        if row["parameter_id"] not in SCALE_IDS:
            continue
        value = Decimal(row["value"])
        scaled = value * factor
        output_rows.append({
            "parameter_id": row["parameter_id"],
            "variable": row["variable"],
            "source_value": str(value),
            "scaled_value": f"{scaled:.6f}",
            "unit": row["unit"],
            "source_geography": row["geography"],
            "source_scope": row["scope"],
            "reference_year": row["reference_year"],
            "source_id": row["source_id"],
            "scaling_factor": f"{factor:.12f}",
            "scaling_rule": "target_population / Beijing_2023_year_end_resident_population",
            "evidence_class": "C",
            "status": "derived_linear_population_scale_not_observed",
            "caveat": (
                "Linear per-capita scaling assumption. Preserve source scope; "
                "operator-level bus values remain operator-scope estimates. "
                "Fractional vehicle counts are mathematical expectations, not literal counts."
            ),
        })

    fields = list(output_rows[0].keys()) if output_rows else []
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Beijing population: {base_population}")
    print(f"Target population: {TARGET_POPULATION}")
    print(f"Linear scaling factor: {factor}")
    print(f"Wrote {len(output_rows)} rows to {OUTPUT}")

if __name__ == "__main__":
    main()
