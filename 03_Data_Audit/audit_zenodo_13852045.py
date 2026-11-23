# -*- coding: utf-8 -*-
"""Audit the two CSVs from Zenodo record 13852045.

Place the original CSV files unchanged in:
  01_Raw_Data/Zenodo_13852045/

Run from repository root:
  python 03_Data_Audit/audit_zenodo_13852045.py

The script does not download source data and never modifies raw files.
"""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "01_Raw_Data" / "Zenodo_13852045"
PROCESSED = ROOT / "02_Cleaned_Data" / "Zenodo_13852045"
LOGS = ROOT / "03_Data_Audit" / "Logs"
PROCESSED.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

FILES = {
    "Fig1e.Daily driving distance of different vehicle types.csv": {
        "expected_md5": "17a1dc8d71af0b3767987eab294c0bc6",
        "expected_sha256": "29c99684e665d0f8139a02bcc10751575d550680b903e26013590f82fac2a05f",
        "kind": "cdf",
    },
    "FigSI5.Distributions of average daily driving distance by vehicle type.csv": {
        "expected_md5": "b66cad7047d3f496adb70e4a99b52058",
        "expected_sha256": "d2af33165824b1d50b318bd41f85fb17555d648abfd0cf09bb3e7ef6a06909cf",
        "kind": "city_boxplot",
    },
}

def file_hashes(path: Path):
    data = path.read_bytes()
    return (
        hashlib.md5(data).hexdigest(),
        hashlib.sha256(data).hexdigest(),
        len(data),
    )

def is_html(path: Path) -> bool:
    head = path.read_bytes()[:512].decode("utf-8-sig", errors="ignore").lstrip().lower()
    return head.startswith("<html") or head.startswith("<!doctype html")

def main():
    report = {
        "audit_time_utc": datetime.now(timezone.utc).isoformat(),
        "source": "Zenodo record 13852045",
        "source_url": "https://zenodo.org/records/13852045",
        "files": {},
    }

    for filename, spec in FILES.items():
        path = RAW / filename
        if not path.exists():
            report["files"][filename] = {"status": "MISSING"}
            continue
        if is_html(path):
            report["files"][filename] = {"status": "REJECT_HTML"}
            continue

        md5, sha256, size = file_hashes(path)
        df_raw = pd.read_csv(path, encoding="utf-8-sig")
        result = {
            "bytes": size,
            "md5": md5,
            "expected_md5": spec["expected_md5"],
            "md5_match": md5 == spec["expected_md5"],
            "sha256": sha256,
            "expected_sha256": spec["expected_sha256"],
            "sha256_match": sha256 == spec["expected_sha256"],
            "raw_rows": int(len(df_raw)),
            "raw_columns": list(df_raw.columns),
        }

        if spec["kind"] == "cdf":
            expected = [
                "CDF Percentile", "Private car", "Official car",
                "SPV", "Rental car", "Bus", "Taxi",
            ]
            result.update({
                "missing_cells": int(df_raw.isna().sum().sum()),
                "duplicate_rows": int(df_raw.duplicated().sum()),
                "columns_match": list(df_raw.columns) == expected,
                "percentile_sequence_1_to_100": (
                    df_raw["CDF Percentile"].tolist() == list(range(1, 101))
                ),
                "monotone_by_vehicle": {
                    c: bool(df_raw[c].is_monotonic_increasing) for c in expected[1:]
                },
                "private_car_quantiles_km": {
                    f"P{p}": float(
                        df_raw.loc[df_raw["CDF Percentile"] == p, "Private car"].iloc[0]
                    )
                    for p in [25, 50, 75, 90, 95, 99]
                },
            })
            df_raw.to_csv(
                PROCESSED / "Fig1e_analysis_copy.csv",
                index=False,
                encoding="utf-8-sig",
            )
            checks = [
                result["md5_match"], result["sha256_match"],
                result["missing_cells"] == 0,
                result["duplicate_rows"] == 0,
                result["columns_match"],
                result["percentile_sequence_1_to_100"],
                all(result["monotone_by_vehicle"].values()),
            ]
        else:
            # Drop only fully empty separator rows from an in-memory analysis copy.
            df = df_raw.dropna(how="all").copy()
            qcols = [
                "Lower Whisker", "Q1 (25%)", "Median (50%)",
                "Q3 (75%)", "Upper Whisker",
            ]
            city_type = df["city_vehicle type"].str.split("_", n=1, expand=True)
            result.update({
                "blank_separator_rows": int(df_raw.isna().all(axis=1).sum()),
                "valid_rows": int(len(df)),
                "missing_cells_valid_rows": int(df.isna().sum().sum()),
                "duplicate_valid_rows": int(df.duplicated().sum()),
                "city_count": int(city_type[0].nunique()),
                "vehicle_category_counts": city_type[1].value_counts().to_dict(),
                "whisker_order_valid": bool(
                    df[qcols].apply(lambda row: row.is_monotonic_increasing, axis=1).all()
                ),
                "unit_warning": "Metadata unit is '-'; confirm figure axis/method before annualization.",
            })
            df.to_csv(
                PROCESSED / "FigSI5_clean_analysis_copy.csv",
                index=False,
                encoding="utf-8-sig",
            )
            checks = [
                result["md5_match"], result["sha256_match"],
                result["blank_separator_rows"] == 42,
                result["valid_rows"] == 42,
                result["missing_cells_valid_rows"] == 0,
                result["duplicate_valid_rows"] == 0,
                result["city_count"] == 7,
                result["whisker_order_valid"],
            ]

        result["status"] = "PASS" if all(checks) else "REVIEW"
        report["files"][filename] = result

    out = LOGS / "Zenodo_13852045_QC_Report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Raw files were not modified.")

if __name__ == "__main__":
    main()
