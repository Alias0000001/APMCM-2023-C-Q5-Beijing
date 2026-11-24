import csv, unittest, xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/"02_Cleaned_Data"; F=R/"09_Paper_Draft"/"figures_final"/"remediation"
def rows(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
class RemediationTests(unittest.TestCase):
    def test_sensitivity(self):
        r=rows(D/"R9_7FIX_SENSITIVITY_ENVELOPE.csv")
        self.assertEqual(len(r),12)
        z=next(x for x in r if x["design"]=="remediation_25_packages" and x["scenario"]=="S4")
        self.assertEqual(int(float(z["sets"])),328050)
        self.assertEqual(int(float(z["negative_sets"])),24)
        self.assertAlmostEqual(float(z["min_reduction_pct"]),-.095129454,places=6)
    def test_road(self):
        r=rows(D/"R9_7FIX_NOX_PRIORITY.csv")[0]
        self.assertEqual(int(float(r["sets"])),590490)
        self.assertEqual(int(float(r["bus_first"])),406290)
        for x in rows(D/"R9_7FIX_ROAD_ENVELOPE.csv"):
            self.assertEqual(int(float(x["sets"])),4133430)
            self.assertEqual(int(float(x["negative_sets"])),0)
    def test_new_figures(self):
        r=rows(F/"MANIFEST.csv"); self.assertEqual(len(r),13)
        for x in r:
            self.assertTrue(x["source"] and x["caption"])
            self.assertTrue(ET.parse(F/x["svg"]).getroot().tag.endswith("svg"))
            self.assertEqual((F/x["png"]).read_bytes()[:8],b"\x89PNG\r\n\x1a\n")
            self.assertEqual((F/x["pdf"]).read_bytes()[:4],b"%PDF")
        for x in rows(F/"LAYOUT_QA.csv"):
            self.assertGreaterEqual(float(x["min_font_pt"]),8)
            self.assertEqual(float(x["native_width_cm"]),15)
            self.assertEqual(int(x["out_of_canvas_text_count"]),0)

    def test_gap_alternatives(self):
        for name,n in [("R9_7FIX_BUS_GAP_SCENARIOS.csv",60),("R9_7FIX_DUST_DIAGNOSTIC.csv",12),("R9_7FIX_PKM_BREAK_EVEN.csv",6),("R9_7FIX_MILEAGE_SOURCE_ALTERNATIVES.csv",30),("R9_7FIX_CHARGER_DIAGNOSTIC.csv",36),("R9_7FIX_NOISE_DIAGNOSTIC.csv",54),("R9_7FIX_GENERATION_POLLUTANTS.csv",24)]:
            data=rows(D/name); self.assertEqual(len(data),n)
        b=rows(D/"R9_7FIX_BUS_GAP_SCENARIOS.csv")
        for x in b:
            if x['scenario']=='S0':self.assertAlmostEqual(float(x['reduction_vs_paired_S0_pct']),0)
        c=rows(D/"R9_7FIX_STAGE_COVERAGE.csv")
        self.assertEqual(len(c),128)
        self.assertEqual(next(x['coverage'] for x in c if x['vehicle']=='bus_BEV' and x['stage']=='replacement_traction_battery'),'SUPPLEMENTARY_PROXY')
        self.assertEqual(next(x['coverage'] for x in c if x['vehicle']=='bus_BEV' and x['stage']=='resuspended_dust'),'SUPPLEMENTARY_PROXY')
        svg=(F/'F05_Road_Pollutants.svg').read_text().lower();self.assertIn('#94aa9c',svg);self.assertIn('#cad8ce',svg);self.assertNotIn('#d3a16f',svg)
