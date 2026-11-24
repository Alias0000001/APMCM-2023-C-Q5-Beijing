import csv,math,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
class Audit02Tests(unittest.TestCase):
    def test_grid(self):
        rows=read("R9_7AUDIT02_PROPULSION_GRID.csv")
        keys=["private_NEV_stock_share","BEV_fraction_of_NEV","mixed_bus_BEV_fraction","NEV_relative_mileage","BEV_bus_relative_mileage"]
        groups={}
        for r in rows:
            groups.setdefault(tuple(r[k] for k in keys),{})[r["scenario"]]=r
            self.assertTrue(0<=float(r["S0_car_BEV_VKT_share"])+float(r["S0_car_PHEV_VKT_share"])<=1)
            self.assertTrue(0<=float(r["S0_bus_BEV_VKT_share"])<=1)
        self.assertEqual(len(rows),1458);self.assertEqual(len(groups),243)
        for g in groups.values():
            self.assertEqual(set(g),{"S-1","S0","S1","S2","S3","S4"})
            v={s:float(r["partial_GWP_kt"]) for s,r in g.items()}
            self.assertAlmostEqual(v["S3"]-v["S2"]-v["S1"]+v["S0"],0,delta=1e-7)
            for s,r in g.items():self.assertAlmostEqual(float(r["paired_reduction_pct"]),100*(1-v[s]/v["S0"]),delta=1e-7)
            self.assertEqual(g["S3"]["production_kt"],g["S4"]["production_kt"])
    def test_reference_and_fossil_alternative(self):
        r=read("R9_7AUDIT02_ALTERNATIVES.csv")
        a={x["scenario"]:x for x in r if x["case"]=="base"}
        b={x["scenario"]:x for x in r if x["case"]=="all_diesel_Sminus1"}
        z=read("R9_7E_ENVIRONMENTAL_MATRIX.csv")
        for x in z:
            s=x["scenario"];self.assertAlmostEqual(float(a[s]["partial_GWP_kt"]),float(x["partial_GWP_kt_y"]),delta=2e-6)
            if s!="S-1":self.assertEqual({k:v for k,v in a[s].items() if k!="case"},{k:v for k,v in b[s].items() if k!="case"})
        self.assertNotEqual(a["S-1"]["NOx_t"],b["S-1"]["NOx_t"])
    def test_envelope(self):
        r=read("R9_7AUDIT02_PROPULSION_GRID.csv");e=read("R9_7AUDIT02_PROPULSION_ENVELOPE.csv")
        for x in e:
            a=[float(y["paired_reduction_pct"]) for y in r if y["scenario"]==x["scenario"]]
            self.assertEqual(len(a),243);self.assertAlmostEqual(min(a),float(x["min_paired_reduction_pct"]),places=7);self.assertAlmostEqual(max(a),float(x["max_paired_reduction_pct"]),places=7)
