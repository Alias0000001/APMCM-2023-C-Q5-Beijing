import csv, math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"07_LCA_LCIA"
rows=[
("diesel_bus",2.25,.27,42.5,400000),
("natural_gas_bus",2.50,.30,40.5,400000),
("diesel_hybrid_bus",2.76,.33,37.5,400000),
("battery_electric_bus",3.06,.40,34.5,400000)]
out=[]
for name,raw,assembly,occ,life in rows:
    manufacture=(raw+assembly)*occ*life/1000
    annualized=manufacture*1000/life
    out.append(dict(technology=name,raw_material_kgCO2e_per_1000_PKM=raw,
      assembly_kgCO2e_per_1000_PKM=assembly,
      manufacturing_kgCO2e_per_1000_PKM=raw+assembly,
      effective_passengers=occ,life_km=life,
      manufacturing_tCO2e_per_bus=manufacture/1000,
      annualized_manufacturing_gCO2e_per_vehicle_km=annualized,
      source="Lin2015_Fig2_Table5",scope="historical raw material + assembly; EOL excluded"))
assert [round(r["manufacturing_tCO2e_per_bus"],3) for r in out]==[42.84,45.36,46.35,47.748]
with (D/"R9_7C_BUS_MANUFACTURING_RECALC.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
phev=[
("PHEV","LFP",56.18,160000,8988.8),
("PHEV","NMC",81.40,120000,9768.0),
("BEV","LFP",73.20,160000,11712.0),
("BEV","NMC",111.36,120000,13363.2)]
for tech,chem,gkm,life,expected in phev:
    calc=gkm*life/1000
    assert math.isclose(calc,expected,abs_tol=.01)
print("PASS: 4 bus manufacturing factors; 4 PHEV/BEV vehicle-cycle totals; PHEV totals explicitly not manufacturing-only")
