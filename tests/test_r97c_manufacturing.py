import csv
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Cleaned_Data"

def rows(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

class R97CManufacturingTests(unittest.TestCase):
    def test_six_scenarios_and_private_ranges(self):
        rs = rows("R9_7C_PRIVATE_MANUFACTURING_SCENARIOS.csv")
        self.assertEqual(len(rs), 6)
        for r in rs:
            lo = float(r["manufacturing_CO2_low_t_y"])
            mid = float(r["manufacturing_CO2_base_t_y"])
            hi = float(r["manufacturing_CO2_high_t_y"])
            self.assertTrue(all(math.isfinite(x) and x >= 0 for x in (lo, mid, hi)))
            self.assertLessEqual(lo, mid)
            self.assertLessEqual(mid, hi)
            self.assertEqual(r["impact_unit"], "CO2 only")

    def test_private_s3_s4_equal(self):
        rs = {r["scenario"]: r for r in rows("R9_7C_PRIVATE_MANUFACTURING_SCENARIOS.csv")}
        self.assertAlmostEqual(float(rs["S3"]["manufacturing_CO2_base_t_y"]),
                               float(rs["S4"]["manufacturing_CO2_base_t_y"]), places=6)

    def test_bus_vkt_conserved_and_s3_s4_equal(self):
        activity = {r["scenario"]: r for r in rows("R9_7A_SIX_SCENARIO_VKT.csv")}
        mfg = {r["scenario"]: r for r in rows("R9_7C_BUS_MANUFACTURING_SCENARIOS.csv")}
        self.assertEqual(len(mfg), 6)
        for s, r in mfg.items():
            total = sum(float(r[k]) for k in (
                "bus_diesel_VKT_km", "bus_natural_gas_VKT_km",
                "bus_hybrid_residual_VKT_km", "bus_BEV_VKT_km",
                "bus_unclassified_VKT_km"))
            self.assertAlmostEqual(total, float(activity[s]["bus_total_vkt_km"]), delta=0.02)
            self.assertGreaterEqual(float(r["bus_manufacturing_GHG_tCO2e_y"]), 0)
        self.assertAlmostEqual(float(mfg["S3"]["bus_manufacturing_GHG_tCO2e_y"]),
                               float(mfg["S4"]["bus_manufacturing_GHG_tCO2e_y"]), places=6)

    def test_bus_factor_derivation(self):
        rs = {r["source_id"] + "_" + r["technology"]: r
              for r in rows("R9_7C_BUS_FACTOR_BOUNDARY_ALTERNATIVES.csv")}
        self.assertAlmostEqual(float(rs["LIN2015_BEV"]["manufacturing_g_per_vehicle_km"]), 119.37, places=5)
        self.assertAlmostEqual(float(rs["YING2018_BEV"]["manufacturing_g_per_vehicle_km"]), 226.3547368421, places=5)

    def test_no_invalid_co2_co2e_grand_total(self):
        with (DATA / "R9_7C_MANUFACTURING_LEDGER.csv").open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            self.assertNotIn("total_manufacturing_t_y", reader.fieldnames)
            rs = list(reader)
        self.assertEqual(len(rs), 6)
        self.assertTrue(all("do not aggregate" in r["aggregation_rule"] for r in rs))

    def test_partial_lca_gwp_reconciles_and_s4_is_lower(self):
        rs = {r["scenario"]: r for r in rows("R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv")}
        self.assertEqual(len(rs), 6)
        self.assertAlmostEqual(float(rs["S0"]["partial_LCA_GWP_t_y"]), 567788.6558, delta=0.02)
        self.assertAlmostEqual(float(rs["S3"]["partial_LCA_GWP_t_y"]), 486977.9085, delta=0.02)
        self.assertAlmostEqual(float(rs["S4"]["partial_LCA_GWP_t_y"]), 341002.0368, delta=0.02)
        self.assertLess(float(rs["S4"]["partial_LCA_GWP_t_y"]), float(rs["S3"]["partial_LCA_GWP_t_y"]))
        for r in rs.values():
            self.assertAlmostEqual(
                float(r["private_vehicle_production_GWP_t_y"]) +
                float(r["bus_manufacturing_GWP_t_y"]) +
                float(r["WTW_operating_GWP_t_y"]),
                float(r["partial_LCA_GWP_t_y"]), delta=0.02)

    def test_bev_manufacturing_source_sensitivity(self):
        rs = {(r["factor_set"], r["scenario"]): r
              for r in rows("R9_7C_PARTIAL_LCA_GWP_SOURCE_SENSITIVITY.csv")}
        self.assertEqual(len(rs), 12)
        self.assertAlmostEqual(float(rs[("QIAO2017_BEV_NMC", "S3")]["partial_LCA_GWP_t_y"]),
                               486977.9085, delta=0.02)
        self.assertAlmostEqual(float(rs[("XIONG2019_BEV_NMC", "S3")]["partial_LCA_GWP_t_y"]),
                               442903.3243, delta=0.02)
        self.assertLess(float(rs[("XIONG2019_BEV_NMC", "S3")]["partial_LCA_GWP_t_y"]),
                        float(rs[("QIAO2017_BEV_NMC", "S3")]["partial_LCA_GWP_t_y"]))

    def test_factor_register_contains_phev_and_bus(self):
        rs = rows("R9_7C_MANUFACTURING_FACTOR_REGISTER.csv")
        ids = {r["source_id"] for r in rs}
        self.assertIn("YANG21_PHEV", ids)
        self.assertIn("XIONG19_PHEV_NMC", ids)
        self.assertIn("LIN15_BUS_BEB", ids)
        self.assertIn("YING18_BUS_BEV", ids)

if __name__ == "__main__":
    unittest.main()
