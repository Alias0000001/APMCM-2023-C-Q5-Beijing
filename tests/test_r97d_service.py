import csv,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/"02_Cleaned_Data"
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
class ServiceTests(unittest.TestCase):
    def test_equal_service(self):
        rs=read(D/"R9_7D_SERVICE_SENSITIVITY.csv")
        self.assertEqual(len(rs),30)
        for r in rs:
            self.assertNotIn(None,r)
            b=next(x for x in rs if x["case"]==r["case"] and x["scenario"]=="S0")
            for mode in ("car","bus"):
                self.assertGreaterEqual(float(r[f"{mode}_effective_pax"]),1)
                self.assertAlmostEqual(float(r[f"equal_service_{mode}_VKT"])*float(r[f"{mode}_effective_pax"]),float(b[f"{mode}_PKM"]),delta=5)
            if r["case"]=="reference":
                self.assertAlmostEqual(float(r["equal_service_partial_GWP_tCO2e"]),float(r["fixed_VKT_partial_GWP_tCO2e"]),delta=.001)
    def test_bus_csv(self):
        rs=read(R/"07_LCA_LCIA/R9_7C_BUS_MANUFACTURING_RECALC.csv")
        self.assertEqual(len(rs),4)
        for r in rs:
            self.assertNotIn(None,r)
            self.assertAlmostEqual(float(r["life_km"])*float(r["effective_passengers"]),float(r["lifetime_PKM_per_bus"]),places=2)
            self.assertAlmostEqual(float(r["manufacturing_tCO2e_per_bus"])*1e6/float(r["life_km"]),float(r["annualized_manufacturing_gCO2e_per_vehicle_km"]),places=5)
    def test_mileage(self):
        rs=read(D/"R9_7D_MILEAGE_DENOMINATOR_SENSITIVITY.csv")
        self.assertEqual(len(rs),6)
        for r in rs:
            self.assertAlmostEqual(float(r["alternative_car_VKT"])*.461,float(r["base_car_VKT"]),delta=.01)
            self.assertGreater(float(r["alternative_partial_GWP_tCO2e"]),float(r["base_partial_GWP_tCO2e"]))
    def test_observed_PKM_remains_missing(self):
        rs=read(D/"R9_7D_PKM_EVIDENCE.csv")
        self.assertEqual(next(r for r in rs if r["indicator"]=="actual_bus_PKM")["value"],"NA")
