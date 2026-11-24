"""R9.7B contest-time WTW operating energy. No vehicle manufacturing or pollutant mass.
Execute after r9_7a_activity_scenarios.py. Standard library only.
"""
import csv,json,math
from pathlib import Path
D=Path(__file__).resolve().parents[1]/"02_Cleaned_Data"
def read(name):
    with (D/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
P={r["parameter"]:float(r["value"]) for r in read("R9_7B_ENERGY_INPUTS.csv")}
assert math.isclose(P["car_e"],P["car_month_kWh"]/P["car_month_km"])
assert math.isclose(P["bus_e"],P["bus_month_kWh"]/P["bus_month_km"])
def calc(r,a):
    x=a["ac_share"]
    ds=a["diesel_off"]+(a["diesel_on"]-a["diesel_off"])*x
    ng=a["gas_off"]+(a["gas_on"]-a["gas_off"])*x
    hy=a["hybrid_off"]+(a["hybrid_on"]-a["hybrid_off"])*x
    md,mg=a["mixed_diesel_share"],a["mixed_gas_share"]
    mh=1-md-mg
    assert mh>=0 and 0<a["eta"]<=1
    u=a["uf"]
    gasoline=(r["private_ICEV_vkt_km"]*a["gasoline_l100"]+r["private_PHEV_vkt_km"]*(1-u)*a["phev_cs_l100"])/100
    ce=(r["private_BEV_vkt_km"]*a["car_e"]+r["private_PHEV_vkt_km"]*u*a["phev_cd_e"])/a["eta"]
    be=r["bus_BEV_vkt_km"]*a["bus_e"]/a["eta"]
    diesel=(r["bus_diesel_vkt_km"]+r["bus_unclassified_vkt_km"]*a["unknown_diesel_share"]+r["bus_mixed_nonBEV_vkt_km"]*md)*ds+r["bus_mixed_nonBEV_vkt_km"]*mh*hy
    gas=(r["bus_natural_gas_vkt_km"]+r["bus_unclassified_vkt_km"]*(1-a["unknown_diesel_share"])+r["bus_mixed_nonBEV_vkt_km"]*mg)*ng
    mj=gasoline*a["gasoline_mj_l"]+diesel+gas+(ce+be)*3.6
    gg=gasoline*a["gasoline_mj_l"]*a["gasoline_ef"]/1e6
    dg=diesel*a["diesel_ef"]/1e6
    ngw=gas*((1-a["lng_share"])*a["cng_ef"]+a["lng_share"]*a["lng_ef"])/1e6
    cg=ce*a["grid_ef"]*r["operating_grid_factor_multiplier"]/1000
    bg=be*a["grid_ef"]*r["operating_grid_factor_multiplier"]/1000
    return [gasoline,diesel,gas,ce,be,mj,gg,dg,ngw,cg,bg,gg+cg,dg+ngw+bg,gg+dg+ngw+cg+bg]
results=[]
for c in read("R9_7B_ENERGY_CASES.csv"):
    a=P|json.loads(c["overrides_json"])
    for r in read("R9_7A_SIX_SCENARIO_VKT.csv"):
        s=r.pop("scenario")
        r={k:float(v) for k,v in r.items()}
        vals=calc(r,a)
        assert all(math.isfinite(v) and v>=0 for v in vals)
        assert math.isclose(vals[-3]+vals[-2],vals[-1],abs_tol=1e-7)
        results.append([c["case"],s]+vals)
for c in {r[0] for r in results}:
    a=next(r for r in results if r[:2]==[c,"S3"])
    b=next(r for r in results if r[:2]==[c,"S4"])
    assert a[2:8]==b[2:8] and math.isclose(b[-1],a[-1]*.5)
with (D/"R9_7B_SIX_SCENARIO_ENERGY_WTW.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,lineterminator="\n")
    w.writerow("case,scenario,gasoline_L,diesel_MJ,natural_gas_MJ,private_electricity_kWh,bus_electricity_kWh,final_energy_MJ,gasoline_WTW_tCO2e,diesel_WTW_tCO2e,natural_gas_WTW_tCO2e,private_electricity_WTW_tCO2e,bus_electricity_WTW_tCO2e,private_WTW_tCO2e,bus_WTW_tCO2e,total_WTW_tCO2e".split(","))
    w.writerows([r[:2]+[f"{v:.6f}" for v in r[2:]] for r in results])
print(f"PASS: {len(results)} rows; nonnegative energy, class GWP reconciliation, S3/S4 policy check")
