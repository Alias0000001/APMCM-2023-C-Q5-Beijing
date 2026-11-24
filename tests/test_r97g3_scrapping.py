import csv,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
class ScrappingTests(unittest.TestCase):
    def test_unit_conversion(self):
        for r in read("R9_7G3_BUS_SCRAPPING_FACTORS.csv"):
            f,o,L,t,g=[float(r[k]) for k in ("source_scrapping_kgCO2e_per_1000_PKM","effective_passengers","lifetime_km","scrapping_tCO2e_per_bus","scrapping_gCO2e_per_vehicle_km")]
            self.assertAlmostEqual(t,f*o*L/1e6)
            self.assertAlmostEqual(g,f*o)
            self.assertAlmostEqual(g,t*1e6/L)
    def test_expansion_and_baseline(self):
        rs=read("R9_7G3_BUS_SCRAPPING_SENSITIVITY.csv")
        self.assertEqual(len(rs),6)
        z=next(float(r["expanded_partial_GWP_tCO2e_y"]) for r in rs if r["scenario"]=="S0")
        for r in rs:
            e,p,t,rp=[float(r[k]) for k in ("bus_scrapping_tCO2e_y","original_partial_GWP_tCO2e_y","expanded_partial_GWP_tCO2e_y","reduction_vs_paired_S0_pct")]
            self.assertGreater(e,0);self.assertAlmostEqual(e+p,t,delta=1e-6)
            self.assertAlmostEqual(100*(1-t/z),rp,places=6)
        self.assertEqual(rs[4]["bus_scrapping_tCO2e_y"],rs[5]["bus_scrapping_tCO2e_y"])
