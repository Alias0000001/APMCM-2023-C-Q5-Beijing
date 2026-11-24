import csv,unittest,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
class TransferTests(unittest.TestCase):
    def test_grid_and_paired_baseline(self):
        rows=read("R9_7F_TRANSFER_GRID.csv")
        self.assertEqual(len(rows),162)
        for r in rows:
            z=next(x for x in rows if all(x[k]==r[k] for k in ("g_ownership","m_mileage","b_bus_supply")) and x["scenario"]=="S0")
            self.assertAlmostEqual(sum(float(r[k]) for k in ("private_WTW_t","bus_WTW_t","private_production_t","bus_production_t")),float(r["partial_GWP_t"]),delta=1e-5)
            self.assertAlmostEqual(100*(1-float(r["partial_GWP_t"])/float(z["partial_GWP_t"])),float(r["reduction_vs_paired_S0_pct"]),places=6)
        base=next(r for r in rows if all(float(r[k])==1 for k in ("g_ownership","m_mileage","b_bus_supply")) and r["scenario"]=="S0")
        self.assertAlmostEqual(float(base["partial_GWP_t"]),567788.6558,delta=.02)
    def test_nested_counts(self):
        a={r["indicator"]:r for r in read("R9_7F_ORDERING_COUNTS.csv")}
        self.assertEqual(int(float(a["partial_GWP"]["sets"])),14580)
        self.assertEqual(int(float(a["partial_GWP"]["preferred_or_strict_order_count"])),14223)
        self.assertEqual(int(float(a["NOx"]["sets"])),432)
        self.assertEqual(int(float(a["NOx"]["preferred_or_strict_order_count"])),337)
    def test_witness_and_ranges(self):
        rows=read("R9_7F_NESTED_ENVELOPE.csv")
        self.assertEqual(len(rows),36)
        s3=next(r for r in rows if r["indicator"]=="partial_GWP_t" and r["scenario"]=="S3")
        s4=next(r for r in rows if r["indicator"]=="partial_GWP_t" and r["scenario"]=="S4")
        self.assertLess(float(s3["min_reduction_pct"]),0)
        self.assertGreater(float(s4["min_reduction_pct"]),0)
        w=read("R9_7F_REVERSAL_WITNESS.csv")[0]
        self.assertAlmostEqual(float(w["S3_reduction_pct"]),float(s3["min_reduction_pct"]),places=6)
        self.assertAlmostEqual(100*(1-float(w["S3_partial_GWP_t"])/float(w["S0_partial_GWP_t"])),float(w["S3_reduction_pct"]),places=6)
    def test_jinhua_diagnostic_is_separate(self):
        rs=read("R9_7F_JINHUA_RETROSPECTIVE_DIAGNOSTIC.csv")
        self.assertEqual(len(rs),18)
        self.assertTrue(all(math.isclose(float(r["g_ownership"]),1.171038) and math.isclose(float(r["b_bus_supply"]),.646917) for r in rs))
