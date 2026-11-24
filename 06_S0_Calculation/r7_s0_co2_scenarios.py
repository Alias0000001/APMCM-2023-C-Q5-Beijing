#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R7 reproducible S0 Beijing 2023 representative 1m-pop city.
Uses R5 published-data activity proxies. Fuel/UF/split scenarios are NOT observations.
CO2 only (electricity consumption + direct fuel combustion); not CO2e, not LCA.
"""
from __future__ import annotations
import csv
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"02_Cleaned_Data"/"R7_S0_CO2_scenarios.csv"
P=1_000_000/21_858_000
BUS=1_151_000_000
FLEET={"diesel":1495,"gas":6795,"electric_drive_mixed":15451,"unclassified":6}
assert sum(FLEET.values())==23747
PRIVATE_TOTAL=5_073_000*28.4*365
NEV=528_000
ICE=4_545_000
GRID=0.5554
EV_CAR_KWH_KM=.160  # 2023-10 private passenger-car row: 16.0 kWh/100km; 15.2 is taxi row
EV_BUS_KWH_KM=.626  # 2023-10 bus row; charging-meter boundary not specified
# Assumed coefficients below: screening stress test, not measured Beijing 2023 means.
GASOLINE_KGCO2_L=2.31
DIESEL_KGCO2_L=2.68
NATGAS_KGCO2_KG=2.75

def calc(phev_share=.05,active_days=300,r=1.,q=.8,uf=.66,
         ice_l100=7.5,diesel_l100=35.,gas_kg100=30.,
         mixed_other_kgco2_km=.9,phev_l100=7.5,phev_kwh100=16.):
    bev_n=NEV*(1-phev_share)
    phev_n=NEV*phev_share
    bev=bev_n*1551.6*12*P
    phev=phev_n*47.1*active_days*P
    ice=(PRIVATE_TOTAL-(bev_n*1551.6*12+phev_n*47.1*active_days))*P
    assert ice>0
    weights={x:n*(r if x=="electric_drive_mixed" else 1.) for x,n in FLEET.items()}
    den=sum(weights.values())
    bus={x:BUS*weights[x]/den*P for x in FLEET}
    assert abs(sum(bus.values())-BUS*P)<1e-4
    e=(bev*EV_CAR_KWH_KM+bus["electric_drive_mixed"]*q*EV_BUS_KWH_KM+
       phev*uf*phev_kwh100/100)
    components={
      "private_ICE_gasoline":ice*ice_l100/100*GASOLINE_KGCO2_L,
      "private_BEV_grid":bev*EV_CAR_KWH_KM*GRID,
      "private_PHEV_gasoline":phev*(1-uf)*phev_l100/100*GASOLINE_KGCO2_L,
      "private_PHEV_grid":phev*uf*phev_kwh100/100*GRID,
      "bus_diesel":bus["diesel"]*diesel_l100/100*DIESEL_KGCO2_L,
      "bus_natural_gas":bus["gas"]*gas_kg100/100*NATGAS_KGCO2_KG,
      "bus_BEV_assumed":bus["electric_drive_mixed"]*q*EV_BUS_KWH_KM*GRID,
      "bus_other_mixed_placeholder":bus["electric_drive_mixed"]*(1-q)*mixed_other_kgco2_km,
    }
    # Do not assign fuel or emission factor to the 6 unclassified April buses.
    co2=sum(components.values())
    return dict(private_total_vkt_km=PRIVATE_TOTAL*P,bus_total_vkt_km=BUS*P,
      private_ICE_vkt_km=ice,private_BEV_vkt_km=bev,private_PHEV_vkt_km=phev,
      bus_diesel_vkt_km=bus["diesel"],bus_gas_vkt_km=bus["gas"],
      bus_BEV_vkt_km_assumed=bus["electric_drive_mixed"]*q,
      bus_other_mixed_vkt_km_assumed=bus["electric_drive_mixed"]*(1-q),
      bus_unclassified_vkt_km=bus["unclassified"],
      electric_kwh=e,co2_tonnes_conditional=co2/1000,
      unclassified_co2="NA", **{k+"_tCO2":v/1000 for k,v in components.items()})

def main():
    scenarios=[("S0_screening",.05,300,1.,.8,.66,7.5,35.,30.,.9),
       ("low_assumptions",0.,250,.8,1.,.79,6.,30.,25.,.6),
       ("high_assumptions",.2396,365,1.2,.6,.66,9.,40.,40.,1.2)]
    # Extra one-at-a-time structural sensitivity on r, q and PHEV share
    for r,q,s in product((.8,1.,1.2),(.6,.8,1.),(0.,.05,.2396)):
        scenarios.append((f"grid_r{r}_q{q}_phev{s}",s,300,r,q,.66,7.5,35.,30.,.9))
    rows=[]
    for name,s,days,r,q,uf,ice_l,diesel_l,gas_kg,other in scenarios:
        row=dict(scenario=name,phev_share_assumed=s,phev_active_days_assumed=days,
                 electric_bus_relative_vkt_assumed=r,bus_BEV_share_in_mixed_assumed=q,
                 phev_electric_vkt_fraction_assumed=uf,
                 private_ICE_l100_assumed=ice_l,bus_diesel_l100_assumed=diesel_l,
                 bus_gas_kg100_assumed=gas_kg,
                 bus_nonBEV_mixed_kgCO2km_assumed=other,
                 boundary="grid_consumption_CO2_plus_tank_combustion_CO2_not_LCA")
        row.update(calc(s,days,r,q,uf,ice_l,diesel_l,gas_kg,other))
        rows.append(row)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    for row in rows[:3]:
        print(row["scenario"],round(row["co2_tonnes_conditional"],1),"t CO2/year",
              "(unclassified bus CO2 excluded)")
    print("Wrote",len(rows),"rows",OUT)
if __name__=="__main__":main()
