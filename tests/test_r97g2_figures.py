import csv,unittest,xml.etree.ElementTree as ET,struct,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]/"09_Paper_Draft"
class FinalFigureTests(unittest.TestCase):
    def test_manifest_and_rendered_pairs(self):
        with (R/"FINAL_FIGURE_MANIFEST.csv").open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),20)
        self.assertEqual(sum(r["domain"]=="contest" for r in rows),11)
        self.assertEqual(len({r["svg"] for r in rows}),20)
        for r in rows:
            root=ET.parse(R/r["svg"]).getroot()
            self.assertTrue(root.tag.endswith("svg"))
            b=(R/r["png"]).read_bytes()
            self.assertEqual(b[:8],b"\x89PNG\r\n\x1a\n")
            w,h=struct.unpack(">II",b[16:24])
            self.assertGreaterEqual(w,1500); self.assertGreaterEqual(h,450)
            self.assertTrue(r["source"] and r["caption"])
    def test_markdown_references(self):
        for filename,domain,count in [("Q5_Contest_Manuscript_EN.md","figures_final",11),("FIGURE_DIAGNOSTIC_APPENDIX.md","figures_diagnostic",9)]:
            links=re.findall(r"!\[[^\]]*\]\(([^)]+)\)",(R/filename).read_text(encoding="utf-8"))
            self.assertEqual(len(links),count)
            for link in links:
                self.assertTrue(link.startswith(domain+"/"))
                self.assertTrue((R/link).exists())
