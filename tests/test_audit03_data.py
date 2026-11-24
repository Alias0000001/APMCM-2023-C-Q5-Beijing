import csv,unittest,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
class Audit03Tests(unittest.TestCase):
    def test_register(self):
        r=read("R9_7AUDIT03_MASTER_PROVENANCE.csv");ids={x["id"]:x for x in r}
        self.assertEqual(len(r),len(ids))
        for pref,name,key in [("A.","R9_7A_CONTEST_ACTIVITY_INPUTS.csv","parameter"),("B.","R9_7B_ENERGY_INPUTS.csv","parameter"),("C.","R9_7C_MANUFACTURING_FACTOR_REGISTER.csv","source_id")]:
            for x in read(name):
                a=ids[pref+x[key]]
                self.assertEqual(float(a["model_value"]),float(x["factor_value" if pref=="C." else "value"]))
                self.assertNotEqual(a["source"],"")
        for x in read("R9_7E_ROAD_FACTORS.csv"):
            for p in ["CO","VOCs","NOx","PM2_5","PM10"]:
                self.assertEqual(float(ids["E."+x["standard"]+"."+x["technology"]+"."+p]["model_value"]),float(x[p]))
        self.assertFalse(any(x["role"]=="MAIN" and x["time_admission"]=="POST" for x in r))
    def test_historical_bus_stress(self):
        r=read("R9_7AUDIT03_BUS_ENERGY_STRESS.csv")
        self.assertEqual(len(r),18)
        for case in set(x["case"] for x in r):
            q={x["scenario"]:x for x in r if x["case"]==case}
            z=float(q["S0"]["partial_GWP_kt"])
            for x in q.values():self.assertAlmostEqual(float(x["paired_reduction_pct"]),100*(1-float(x["partial_GWP_kt"])/z))
            self.assertEqual(q["S3"]["final_energy_PJ"],q["S4"]["final_energy_PJ"])
