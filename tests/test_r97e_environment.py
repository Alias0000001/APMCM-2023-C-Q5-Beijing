import csv,math,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
class EnvironmentalTests(unittest.TestCase):
    def test_factors_and_cases(self):
        fs=read("R9_7E_ROAD_FACTORS.csv")
        self.assertEqual(len(fs),9)
        self.assertEqual(len(read("R9_7E_ROAD_CASES.csv")),8)
        for r in fs:
            self.assertNotIn(None,r)
            self.assertEqual(r["unit"],"g/vehicle-km")
            self.assertGreaterEqual(float(r["PM10"]),float(r["PM2_5"]))
    def test_scenarios_and_class_reconciliation(self):
        rs=read("R9_7E_ROAD_POLLUTANT_SCENARIOS.csv")
        self.assertEqual(len(rs),240)
        self.assertEqual(len({(r["case"],r["scenario"],r["pollutant"]) for r in rs}),240)
        for r in rs:
            a,b,t=[float(r[k]) for k in ("private_t_y","bus_t_y","total_t_y")]
            self.assertGreaterEqual(min(a,b,t),0)
            self.assertAlmostEqual(a+b,t,delta=2e-8)
            if r["scenario"] in ("S3","S4"):
                self.assertEqual(t,0)
            if r["scenario"]=="S1": self.assertEqual(b,0)
            if r["scenario"]=="S2": self.assertEqual(a,0)
    def test_gwp_separation_and_missing_flows(self):
        rs=read("R9_7E_ENVIRONMENTAL_MATRIX.csv")
        self.assertEqual(len(rs),6)
        for r in rs:
            self.assertAlmostEqual(float(r["WTW_GWP_kt_y"])+float(r["production_GWP_kt_y"]),float(r["partial_GWP_kt_y"]),delta=2e-8)
            for k in ("nonexhaust_PM","full_life_cycle_GWP","full_life_cycle_pollutants"): self.assertEqual(r[k],"NA")
    def test_reference_NOx_and_additivity(self):
        rs={r["scenario"]:float(r["road_NOx_t_y"]) for r in read("R9_7E_ENVIRONMENTAL_MATRIX.csv")}
        self.assertAlmostEqual(rs["S0"],364.259080726,places=6)
        self.assertAlmostEqual(rs["S0"]-rs["S1"],rs["S2"],places=6)
        self.assertAlmostEqual(rs["S0"]-rs["S2"],rs["S1"],places=6)
        self.assertEqual(rs["S3"],rs["S4"])
