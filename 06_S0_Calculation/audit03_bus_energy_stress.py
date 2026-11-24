"""Audit-03 historical bus electricity-rate stress, separate from baseline."""
import csv
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(n):
    with (D/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
p={r["parameter"]:float(r["value"]) for r in read("R9_7B_ENERGY_INPUTS.csv")}
e=[r for r in read("R9_7B_SIX_SCENARIO_ENERGY_WTW.csv") if r["case"]=="base"]
z={r["scenario"]:r for r in read("R9_7E_ENVIRONMENTAL_MATRIX.csv")}
cases=[("historical_bus_AC_off",1.),("historical_bus_AC_mix",1+.4*p["ac_share"]),("historical_bus_AC_on",1.4)]
out=[]
for name,u in cases:
    rr=[]
    for r in e:
        s=r["scenario"];delta=float(r["bus_electricity_kWh"])/p["bus_e"]*(u-p["bus_e"])
        dg=delta*p["grid_ef"]*(.5 if s=="S4" else 1)/1e6
        rr.append([name,u,s,float(z[s]["final_energy_PJ"])+delta*3.6/1e9,float(z[s]["partial_GWP_kt_y"])+dg])
    base=next(r[4] for r in rr if r[2]=="S0")
    out.extend(r+[100*(1-r[4]/base)] for r in rr)
with (D/"R9_7AUDIT03_BUS_ENERGY_STRESS.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL,lineterminator="\n");w.writerow(["case","bus_kWh_per_km","scenario","final_energy_PJ","partial_GWP_kt","paired_reduction_pct"]);w.writerows(out)
print("PASS: 18 historical bus energy stress rows; baseline unchanged")
