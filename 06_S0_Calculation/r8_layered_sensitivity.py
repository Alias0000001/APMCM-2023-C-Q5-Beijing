#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R8 three-layer sensitivity: R7 parameter OAT, city-activity transfer, nested stress.
Run: python 06_S0_Calculation/r8_layered_sensitivity.py
CO2 screening only; NOT full LCA/LCIA, probabilistic uncertainty, or Huzhou calibration.
"""
from __future__ import annotations
import csv
from pathlib import Path
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / '02_Cleaned_Data'
SCALE = 1_000_000 / 21_858_000
BUS_VKT = 1_151_000_000
COUNTS = {'diesel': 1495, 'gas': 6795, 'mixed': 15451, 'unknown': 6}
BASE = dict(private_daily_km=28.4, ice_l100=7.5, bev_annual_multiplier=1.0,
            phev_share=0.05, bev_kwh100=15.2, grid_kg_kwh=0.5554,
            bus_relative_vkt=1.0, bus_bev_fraction=0.8, bus_gas_kg100=30.0,
            bus_diesel_l100=35.0, mixed_other_kgco2_km=0.9, phev_uf=0.66)
BOUNDS = {
    'private_daily_km': (25.56, 31.24),
    'ice_l100': (6.0, 9.0), 'bev_annual_multiplier': (0.8, 1.2),
    'phev_share': (0.0, 0.2396), 'bev_kwh100': (12.92, 17.48),
    'grid_kg_kwh': (0.45, 0.65), 'bus_relative_vkt': (0.8, 1.2),
    'bus_bev_fraction': (0.6, 1.0), 'bus_gas_kg100': (25.0, 40.0),
    'bus_diesel_l100': (30.0, 40.0),
    'mixed_other_kgco2_km': (0.6, 1.2), 'phev_uf': (0.5, 0.79)
}

def calc_a(x):
    nbev = 528_000 * (1 - x['phev_share'])
    nphev = 528_000 * x['phev_share']
    bev = nbev * 1551.6 * 12 * x['bev_annual_multiplier'] * SCALE
    phev = nphev * 47.1 * 300 * SCALE
    total_car = 5_073_000 * x['private_daily_km'] * 365 * SCALE
    ice = total_car - bev - phev
    assert ice >= 0, 'ICE residual became negative'
    weights = {k: n*(x['bus_relative_vkt'] if k == 'mixed' else 1)
               for k,n in COUNTS.items()}
    denominator = sum(weights.values())
    v = {k: BUS_VKT*SCALE*w/denominator for k,w in weights.items()}
    assert abs(sum(v.values()) - BUS_VKT*SCALE) < 1e-5
    car = (ice*(x['ice_l100']/100)*2.31
           + bev*(x['bev_kwh100']/100)*x['grid_kg_kwh']
           + phev*((1-x['phev_uf'])*0.075*2.31
                   + x['phev_uf']*0.16*x['grid_kg_kwh']))/1000
    bus = (v['diesel']*(x['bus_diesel_l100']/100)*2.68
           + v['gas']*(x['bus_gas_kg100']/100)*2.75
           + v['mixed']*(x['bus_bev_fraction']*0.626*x['grid_kg_kwh']
             + (1-x['bus_bev_fraction'])*x['mixed_other_kgco2_km']))/1000
    # The April snapshot's 6 unclassified buses retain VKT but have no CO2 assigned.
    return dict(car_t=car,bus_t=bus,total_t=car+bus,
                unclassified_bus_vkt_km=v['unknown'])

def scaled(res,g=1.,m=1.,b=1.):
    return res['car_t']*g*m + res['bus_t']*b

def save(path,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def run():
    baseline=calc_a(BASE)
    with (DATA/'R7_S0_CO2_scenarios.csv').open(encoding='utf-8-sig',newline='') as f:
        old=next(r for r in csv.DictReader(f) if r['scenario']=='S0_screening')
    assert abs(baseline['total_t']-float(old['co2_tons_conditional']))<1e-6
    aa=[dict(scenario='A_baseline',axis='none',value='',
             car_t=baseline['car_t'],bus_t=baseline['bus_t'],
             total_t=baseline['total_t'],delta_pct=0.)]
    ranks=[]
    configs=[('A_baseline',BASE)]
    for field,(low,high) in BOUNDS.items():
        outputs=[]
        for tag,value in [('low',low),('high',high)]:
            p=dict(BASE);p[field]=value
            rr=calc_a(p)
            configs.append((f'A_{field}_{tag}',p))
            aa.append(dict(scenario=f'A_{field}_{tag}',axis=field,value=value,
                           car_t=rr['car_t'],bus_t=rr['bus_t'],total_t=rr['total_t'],
                           delta_pct=100*(rr['total_t']/baseline['total_t']-1)))
            outputs.append(rr['total_t'])
        pmin=dict(BASE);pmax=dict(BASE)
        pmin[field]=BASE[field]*.9
        pmax[field]=BASE[field]*1.1
        elasticity=(calc_a(pmax)['total_t']-calc_a(pmin)['total_t'])/baseline['total_t']/.2
        ranks.append(dict(parameter=field,base_value=BASE[field],test_low=low,test_high=high,
                          co2_low_t=outputs[0],co2_high_t=outputs[1],
                          max_abs_delta_percent=max(abs(z/baseline['total_t']-1)*100 for z in outputs),
                          local_elasticity_10pct=elasticity,
                          interval_kind='ILLUSTRATIVE_STRESS_VALUES_NOT_STATISTICAL_CI'))
    ranks.sort(key=lambda r:r['max_abs_delta_percent'],reverse=True)
    save(DATA/'R8_A_OAT.csv',aa)
    save(DATA/'R8_A_RANKING.csv',ranks)
    bb=[]
    for field in ('g_car_ownership','m_car_mileage','b_bus_vkt'):
        for value in (.8,1.,1.2):
            params=dict(g_car_ownership=1.,m_car_mileage=1.,b_bus_vkt=1.)
            params[field]=value
            bb.append(dict(case=f'B_{field}_{value}',kind='HYPOTHETICAL_STRESS',**params,
                           co2_t=scaled(baseline,params['g_car_ownership'],
                                              params['m_car_mileage'],params['b_bus_vkt'])))
    diagnostics=[
       ('Huzhou_bus_group_unaligned','b_bus_vkt',(61_000_000/1_600_000)/(BUS_VKT/21_858_000)),
       ('Jinhua_bus_group_unaligned','b_bus_vkt',(51_030_000/1_498_000)/(BUS_VKT/21_858_000)),
       ('Jinhua_car_stock_provincial_proxy','g_car_ownership',
        (430747*((18028778+50341)/19127678)/1498000)/(5073000/21858000)),
       ('National_2023_car_mileage_proxy','m_car_mileage',10220/(28.4*365)),
       ('Six_city_2017_car_mileage_proxy','m_car_mileage',12000/(28.4*365))
    ]
    for name,field,value in diagnostics:
        p=dict(g_car_ownership=1.,m_car_mileage=1.,b_bus_vkt=1.)
        p[field]=value
        bb.append(dict(case=name,kind='CROSS_SOURCE_DIAGNOSTIC_NOT_LOCAL_CALIBRATION',
                       **p,co2_t=scaled(baseline,p['g_car_ownership'],
                                                p['m_car_mileage'],p['b_bus_vkt'])))
    save(DATA/'R8_B_TRANSFER_OAT_AND_DIAGNOSTICS.csv',bb)
    nested=[]
    for name,p in configs:
        r=calc_a(p)
        for g,m,b in product((.8,1.,1.2),repeat=3):
            nested.append(dict(a_scenario=name,b_ownership=g,b_mileage=m,b_bus=b,
                               car_t_after_transfer=r['car_t']*g*m,
                               bus_t_after_transfer=r['bus_t']*b,
                               total_t=scaled(r,g,m,b),
                               label='JOINT_STRESS_NOT_PROBABILISTIC_CI'))
    save(DATA/'R8_C_NESTED_GRID.csv',nested)
    assert len(aa)==25 and len(ranks)==12 and len(bb)==14 and len(nested)==675
    assert abs(scaled(baseline)-baseline['total_t'])<1e-9
    print('Baseline tCO2:',round(baseline['total_t'],5))
    print('Rows A OAT/ranking B diagnostics C nested:',len(aa),len(ranks),len(bb),len(nested))
    print('Largest A parameters:',[(r['parameter'],round(r['max_abs_delta_percent'],2)) for r in ranks[:5]])
    print('Nested stress min/max tCO2:',
          round(min(r['total_t'] for r in nested),2),
          round(max(r['total_t'] for r in nested),2))

if __name__=='__main__':run()
