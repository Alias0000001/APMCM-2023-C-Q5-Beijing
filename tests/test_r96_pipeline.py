import csv
import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Cleaned_Data"
LCA = ROOT / "07_LCA_LCIA"
FIG = ROOT / "09_Paper_Draft" / "figures"

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def one(items, key, value):
    return next(r for r in items if r[key] == value)

class R96DataAuditTests(unittest.TestCase):
    def test_private_bev_energy_row_corrected(self):
        r7_script = (ROOT / "06_S0_Calculation" / "r7_s0_co2_scenarios.py").read_text(encoding="utf-8")
        car_script = (ROOT / "06_S0_Calculation" / "r9_lci_passenger_car_module.py").read_text(encoding="utf-8")
        foreground_script = (ROOT / "06_S0_Calculation" / "r9_lci_foreground.py").read_text(encoding="utf-8")
        self.assertIn("EV_CAR_KWH_KM=.160", r7_script)
        self.assertIn("BEV_KWH_KM = 0.160", car_script)
        self.assertIn("CAR_KWH_KM = 0.160", foreground_script)
        ledger = rows(LCA / "R9_LCI_PARAMETER_LEDGER.csv")
        self.assertAlmostEqual(float(one(ledger, "parameter_id", "R9_PVT_BEV_KWH100")["value"]), 16.0)

    def test_r7_energy_reconciliation_uses_canonical_fields(self):
        r7 = one(rows(DATA / "R7_S0_CO2_scenarios.csv"), "scenario", "S0_screening")
        bev = float(r7["private_bev_vkt_km"])
        phev = float(r7["phev_vkt_km"])
        bus_bev = float(r7["bus_bev_vkt_km_assumed"])
        expected = bev * 0.160 + bus_bev * 0.626 + phev * 0.66 * 16.0 / 100
        self.assertTrue(math.isclose(float(r7["electric_kwh"]), expected, rel_tol=1e-8, abs_tol=1e-3))
        for key in ("ice_vkt_km", "private_bev_vkt_km", "phev_vkt_km",
                    "bus_bev_vkt_km_assumed", "bus_nonbev_mixed_vkt_km", "bus_unknown_vkt_km"):
            self.assertIn(key, r7)

    def test_r95_grid_sensitivity_uses_corrected_bev_energy(self):
        data = rows(LCA / "R9_5_GRID_FACTOR_SENSITIVITY.csv")
        r = next(x for x in data if x["scenario"] == "Peng2017_Table8_WTW" and x["vehicle"] == "BEV_NMC")
        expected = 0.160 * 0.73224 * 1000
        self.assertTrue(math.isclose(float(r["electricity_component_g_per_km"]), expected, rel_tol=1e-8))

    def test_bus_manufacturing_proxy_is_historical_and_reproducible(self):
        data = rows(LCA / "R9_6_BUS_MANUFACTURING_FACTOR_EVIDENCE.csv")
        self.assertEqual(len(data), 4)
        expected = {"CDB_diesel": 42.84, "NGB_natural_gas": 45.36,
                    "DHEB_diesel_hybrid": 46.35, "BEB_battery_electric": 47.748}
        for vehicle, value in expected.items():
            r = one(data, "bus_type", vehicle)
            self.assertTrue(math.isclose(float(r["manufacturing_tCO2e_per_bus"]), value, abs_tol=1e-9))
            self.assertEqual(r["status"], "DERIVED_HISTORICAL_MANUFACTURING_PROXY")
            self.assertEqual(r["reference_year"], "2011-2014")

    def test_bus_pkm_is_not_fabricated(self):
        data = rows(LCA / "R9_6_PKM_EVIDENCE_REGISTER.csv")
        self.assertEqual(one(data, "record_id", "PKM08")["value"], "NA")
        ratio = float(one(data, "record_id", "PKM03")["value"])
        expected = 2086870000 / 1151000000
        self.assertTrue(math.isclose(ratio, expected, rel_tol=0, abs_tol=0.001))
        self.assertIn("not average occupancy", one(data, "record_id", "PKM03")["note"])

    def test_meter_point_remains_explicitly_unresolved(self):
        data = rows(LCA / "R9_6_R7_ENERGY_BOUNDARY_AUDIT.csv")
        car = one(data, "vehicle_class", "private_BEV")
        bus = one(data, "vehicle_class", "electric_bus")
        self.assertAlmostEqual(float(car["corrected_model_kWh_per_km"]), 0.160)
        self.assertAlmostEqual(float(bus["corrected_model_kWh_per_km"]), 0.626)
        self.assertIn("METER_POINT_UNSPECIFIED", car["measurement_boundary_status"])
        self.assertIn("METER_POINT_UNSPECIFIED", bus["measurement_boundary_status"])
        self.assertEqual(len(rows(LCA / "R9_6_CHARGING_LOSS_SENSITIVITY.csv")), 6)

    def test_coverage_matrix_retains_historical_proxy_status(self):
        data = rows(LCA / "R9_4_STAGE_COVERAGE_MATRIX.csv")
        self.assertEqual(len(data), 88)
        statuses = {r["coverage_status"] for r in data}
        self.assertIn("HISTORICAL_GWP_PROXY_ONLY", statuses)
        self.assertIn("HISTORICAL_REFERENCE_ONLY", statuses)
        self.assertTrue(all(r["fully_modelled_cradle_to_grave"] == "NO" for r in data))

class R96FigureTests(unittest.TestCase):
    def test_all_figures_exist_and_are_well_formed_svg(self):
        names = [
            "Fig_R9_4_Physical_Inventory_Stage.svg",
            "Fig_R9_5_Grid_Sensitivity.svg",
            "Fig_R9_5_Lifetime_Sensitivity.svg",
            "Fig_R9_5_BreakEven.svg",
            "Fig_R9_5_Battery_Factor_Sensitivity.svg",
            "Fig_R9_6_Coverage_Matrix.svg",
            "Fig_R9_6_Multi_Pollutant_Inventory.svg",
            "Fig_R9_6_Grid_Lifetime_Heatmap.svg",
            "Fig_R9_6_Battery_ReCiPe_Profile.svg",
            "Fig_R9_6_Bus_Manufacturing_Evidence.svg",
            "Fig_R9_6_Energy_Meter_Boundary.svg",
            "Fig_R9_6_PKM_Evidence_Status.svg",
        ]
        for name in names:
            path = FIG / name
            self.assertTrue(path.exists(), name)
            root = ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith("svg"), name)
            self.assertTrue(root.attrib.get("viewBox"), name)
            self.assertGreater(path.stat().st_size, 1500, name)

    def test_figure_manifest_lists_all_12_outputs(self):
        manifest = rows(FIG / "R9_6_FIGURE_MANIFEST.csv")
        self.assertEqual(len(manifest), 12)
        self.assertEqual({r["figure"] for r in manifest}, {"3","5","6","7","8","9","10","11","12","13","14","15"})

if __name__ == "__main__":
    unittest.main(verbosity=2)
