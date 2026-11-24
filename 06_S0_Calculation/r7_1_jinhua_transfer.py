#!/usr/bin/env python3
"""R7.1: city transfer activity-only stress tests; R7 coefficients fixed."""
import csv
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"02_Cleaned_Data"
with (D/"R7_S0_CO2_scenarios.csv").open(encoding="utf-8-sig",newline="") as f:
    s=next(x for x in csv.DictReader(f) if x["scenario"]=="S0_screening")
Ecar=sum(float(s[x]) for x in ("co2_private_ice_t","co2_private_bev_t","co2_private_phev_fuel_t","co2_private_phev_grid_t"))
Ebus=sum(float(s[x]) for x in ("co2_bus_diesel_t","co2_bus_gas_t","co2_bus_bev_t","co2_bus_other_t"))
proxy_share=(18028778+50341)/19127678
jinhua_proxy=430747*proxy_share
g=(jinhua_proxy/1498000)/(5073000/21858000)
b_diag=(51030000/1498000)/(1151000000/21858000)
rows=[]
for m,b in product((.8,1.,1.2),(b_diag,1.,1.2)):
    rows.append(dict(scenario=f"m{m}_b{b:.6f}",private_ownership_multiplier=g,private_mileage_multiplier=m,
        private_total_multiplier=g*m,bus_vkt_multiplier=b,
        bus_data_status="UNALIGNED_GROUP_DIAGNOSTIC" if abs(b-b_diag)<1e-9 else "HYPOTHETICAL",
        car_co2_t=Ecar*g*m,bus_co2_t=Ebus*b,combined_co2_t=Ecar*g*m+Ebus*b,
        evidence_status="EXPLORATORY_NOT_JINHUA_OBSERVED_CO2"))
out=D/"R7_1_Jinhua_transfer_grid.csv"
with out.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert len(rows)==9
print("JH passenger-car proxy",round(jinhua_proxy),"ownership factor",g,"bus unaligned factor",b_diag)
print("Output:",out)
