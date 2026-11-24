import csv,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
class Audit04Tests(unittest.TestCase):
    def test_wear(self):
        r=read("R9_7AUDIT04_WEAR_SCENARIOS.csv");self.assertEqual(len(r),84)
        for x in r:
            self.assertAlmostEqual(sum(float(x[k]) for k in ("private_wear_t_y","bus_wear_t_y","combustion_t_y")),float(x["covered_road_PM_t_y"]))
            b=next(y for y in r if y["case"]==x["case"] and y["pollutant"]==x["pollutant"] and y["scenario"]=="S0")
            self.assertAlmostEqual(float(x["paired_reduction_pct"]),100*(1-float(x["covered_road_PM_t_y"])/float(b["covered_road_PM_t_y"])))
            if x["scenario"] in ("S3","S4"):
                self.assertEqual(float(x["combustion_t_y"]),0);self.assertGreater(float(x["covered_road_PM_t_y"]),0)
    def test_battery(self):
        r=read("R9_7AUDIT04_BATTERY_RECIPE.csv");self.assertEqual(len(r),132)
        for x in r:
            self.assertAlmostEqual(float(x["total_private_battery_amount"]),float(x["annual_equivalent_capacity_kWh"])*float(x["factor_per_kWh"]),delta=1e-7)
            if x["scenario"]=="S-1":self.assertEqual(float(x["total_private_battery_amount"]),0)
            if x["scenario"]=="S3":
                y=next(y for y in r if y["scenario"]=="S4" and y["indicator"]==x["indicator"] and y["recycling_case"]==x["recycling_case"])
                self.assertEqual(x["total_private_battery_amount"],y["total_private_battery_amount"])
    def test_replacement(self):
        r=read("R9_7AUDIT04_REPLACEMENT_STRESS.csv");self.assertEqual(len(r),18)
        z={x["scenario"]:float(x["partial_GWP_kt_y"]) for x in read("R9_7E_ENVIRONMENTAL_MATRIX.csv")}
        for x in r:self.assertAlmostEqual(float(x["expanded_partial_GWP_kt"]),z[x["scenario"]]+float(x["additional_GWP_kt"]))
        c=read("R9_7AUDIT04_STAGE_COVERAGE.csv");self.assertEqual(len(c),128);self.assertTrue(all(x["full_LCA_allowed"]=="NO" for x in c))
