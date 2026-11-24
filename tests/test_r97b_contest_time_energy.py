import csv,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/"02_Cleaned_Data"
def rows(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
class ContestTimeEnergyTests(unittest.TestCase):
    def test_private_bev_reconstruction(self):
        r=rows("R9_7B_PRIVATE_BEV_ENERGY_RECONSTRUCTION.csv")
        self.assertEqual(len(r),10)
        self.assertEqual(sum(int(x["beijing_sample"]) for x in r),44047)
        nominal=sum(int(x["beijing_sample"])*float(x["nominal_kWh_per_100km"]) for x in r)/44047/100
        actual=sum(int(x["beijing_sample"])*float(x["reconstructed_real_world_kWh_per_100km"]) for x in r)/44047/100
        self.assertAlmostEqual(nominal,0.13211265239403364,places=10)
        self.assertAlmostEqual(actual,0.15839046270488116,places=10)
        car8=next(x for x in r if x["model"]=="Car 8")
        self.assertEqual(car8["derivation_method"],"ICCT_Fig4_all_city_energy_delta")
    def test_bus_energy_equivalent_conversion(self):
        p={x["parameter"]:float(x["value"]) for x in rows("R9_7B_BUS_ENERGY_DERIVATION.csv")}
        self.assertAlmostEqual(p["electric_bus_energy_equivalent"]*p["diesel_equivalent_LHV"]/p["MJ_per_kWh"]/100,1.41)
    def test_main_energy_input_not_post_cutoff(self):
        p={x["parameter"]:x for x in rows("R9_7B_ENERGY_INPUTS.csv")}
        self.assertAlmostEqual(float(p["car_e"]["value"]),0.15839046270488116)
        self.assertAlmostEqual(float(p["bus_e"]["value"]),1.41)
        self.assertAlmostEqual(float(p["eta"]["value"]),0.92)
        for k in ["car_month_km","car_month_kWh","bus_month_km","bus_month_kWh"]:
            self.assertEqual(p[k]["status"],"POST_CUTOFF_RETROSPECTIVE_ONLY")
