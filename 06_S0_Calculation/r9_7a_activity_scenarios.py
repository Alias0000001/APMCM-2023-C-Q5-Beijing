"""Contest-time activity reconstruction only; no emissions calculation.
Inputs: R9_7A_CONTEST_ACTIVITY_INPUTS.csv. Outputs: R9_7A_SIX_SCENARIO_VKT.csv.
2022 activity anchor plus 2023 April bus structure; not observed 2023 annual totals.
"""
import csv, math
from pathlib import Path
D = Path(__file__).resolve().parents[1] / "02_Cleaned_Data"
with (D / "R9_7A_CONTEST_ACTIVITY_INPUTS.csv").open(encoding="utf-8-sig", newline="") as f:
    p = {r["parameter"]: float(r["value"]) for r in csv.DictReader(f)}
scale = p["target_population"] / p["reference_population"]
V = p["private_small_micro_cars"] * scale * p["private_daily_distance"] * p["central_city_dispatch_rate"] * 365 * p["ownership_transfer"] * p["mileage_transfer"]
B = p["bus_vkt"] * scale * p["bus_supply_transfer"]
s, t, q = (p[x] for x in ("private_nev_share", "private_bev_fraction_of_nev", "bus_bev_fraction_of_mixed"))
assert p["relative_technology_vkt"] == 1, "unequal technology mileage needs explicit renormalization"
assert all(0 <= x <= 1 for x in (s,t,q))
d,g,m,n = (p[x] for x in ("bus_diesel_count","bus_gas_count","bus_mixed_count","bus_total_count"))
u = n-d-g-m
assert u >= 0
c0 = [V*(1-s), V*s*t, V*s*(1-t)]
b0 = [B*d/n, B*g/n, B*m/n*(1-q), B*m/n*q, B*u/n]
fossil = [B*d/(d+g), B*g/(d+g), 0, 0, 0]
ec, eb = [0,V,0], [0,0,0,B,0]
scenarios = [("S-1",[V,0,0],fossil,1), ("S0",c0,b0,1), ("S1",c0,eb,1), ("S2",ec,b0,1), ("S3",ec,eb,1), ("S4",ec,eb,p["S4_grid_factor_multiplier"])]
header = "scenario,private_total_vkt_km,bus_total_vkt_km,private_ICEV_vkt_km,private_BEV_vkt_km,private_PHEV_vkt_km,bus_diesel_vkt_km,bus_natural_gas_vkt_km,bus_mixed_nonBEV_vkt_km,bus_BEV_vkt_km,bus_unclassified_vkt_km,operating_grid_factor_multiplier".split(",")
with (D / "R9_7A_SIX_SCENARIO_VKT.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,lineterminator="\n")
    w.writerow(header)
    for name,c,b,k in scenarios:
        assert all(x>=0 for x in c+b)
        assert math.isclose(sum(c),V,abs_tol=1e-5)
        assert math.isclose(sum(b),B,abs_tol=1e-5)
        w.writerow([name]+[f"{x:.6f}" for x in [V,B]+c+b+[k]])
assert scenarios[-1][1:3] == scenarios[-2][1:3]
print("PASS: six scenario allocations; class VKT conserved; S3/S4 same activity")
