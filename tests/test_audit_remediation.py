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
