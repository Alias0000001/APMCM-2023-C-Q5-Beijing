#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.5 sensitivity and break-even analysis for the gated two-stage GWP model.

Run from repository root:
    python 06_S0_Calculation/r9_5_sensitivity.py

The strict comparison track uses only Peng2017 WTW electricity factors and
Qiao2017 vehicle manufacturing factors. MEE 2023 factors are post-contest
retrospective checks with explicitly different scopes; they are never silently
substituted into the strict WTW baseline.
Battery-only scenarios are reported separately and never added to Qiao vehicle
manufacturing because Qiao's BEV cradle-to-gate factor already includes its
initial traction battery.
"""
from pathlib import Path
import csv, math

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'07_LCA_LCIA'
OUT=D
R7=ROOT/'02_Cleaned_Data'/'R7_S0_CO2_scenarios.csv'
GRID=D/'R9_5_GRID_FACTOR_REGISTER.csv'
BAT=D/'R9_5_BATTERY_FACTOR_REGISTER.csv'
USE=D/'R9_LCI_PASSENGER_USE_ENERGY.csv'
MFG=D/'R9_LCI_VEHICLE_MANUFACTURING_PROXY.csv'

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))
def num(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (TypeError,ValueError):
        return None
def write(name,rows):
    if not rows: raise ValueError('empty output '+name)
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
def close(a,b,tol=1e-7):
    return math.isclose(a,b,rel_tol=tol,abs_tol=tol)
def main():
    base=next(x for x in read(R7) if x['scenario']=='S0_screening')
    use={x['vehicle']:x for x in read(USE)}
    mfg={x['vehicle_class']:x for x in read(MFG)}
    grids=read(GRID); batteries=read(BAT)
    vkt={'ICEV':num(base['ice_vkt_km']),'BEV':num(base['private_bev_vkt_km']),
         'PHEV':num(base['phev_vkt_km'])}
    gas_l_km=num(use['ICEV']['gasoline_L'])/vkt['ICEV']
    bev_kwh_km=num(use['BEV']['electricity_kWh'])/vkt['BEV']
    gas_kg_km=gas_l_km*0.74*43.07*90.2/1000
    manufacture={'ICEV':9985.0,'BEV_NMC':15005.0,'BEV_LFP':15174.0}
    activity={'ICEV':vkt['ICEV'],'BEV_NMC':vkt['BEV'],'BEV_LFP':vkt['BEV']}
    strict=[x for x in grids if x['scope']=='WTW_CO2e']
    default=next(x for x in strict if x['scenario_id']=='Peng2017_Table8_WTW')
    default_ef=num(default['value'])
    ice_intensity=(manufacture['ICEV']/200000+gas_kg_km)*1000

    lifetime=[]
    for life in (100000,150000,200000,250000,300000):
        for vehicle in ('ICEV','BEV_NMC','BEV_LFP'):
            e=gas_kg_km if vehicle=='ICEV' else bev_kwh_km*default_ef
            m=manufacture[vehicle]/life
            intensity=(m+e)*1000
            lifetime.append(dict(vehicle=vehicle,lifetime_km=life,
                manufacturing_gCO2e_per_km=m*1000,energy_WTW_gCO2e_per_km=e*1000,
                two_stage_gCO2e_per_km=intensity,
                annual_manufacturing_tCO2e=activity[vehicle]*m/1000,
                annual_energy_WTW_tCO2e=activity[vehicle]*e/1000,
                annual_two_stage_tCO2e=activity[vehicle]*(m+e)/1000,
                comparison_scope='Qiao vehicle production + Peng2017 Table8 WTW',
                status='TWO_STAGE_SCREENING_NOT_FULL_LCA'))
    write('R9_5_LIFETIME_SENSITIVITY.csv',lifetime)

    grid_sensitivity=[]
    for factor in grids:
        ef=num(factor['value'])
        if factor['scope']=='generation_only_CO2':
            continue
        for vehicle in ('BEV_NMC','BEV_LFP'):
            m=manufacture[vehicle]/200000
            e=bev_kwh_km*ef
            total=(m+e)*1000
            eligible=factor['eligibility']=='STRICT_PRE_2023_LITERATURE'
            grid_sensitivity.append(dict(scenario=factor['scenario_id'],scope=factor['scope'],
                geography=factor['geography'],factor_kg_per_kWh=ef,vehicle=vehicle,
                manufacturing_gCO2e_per_km=m*1000,electricity_component_g_per_km=e*1000,
                combined_screening_g_per_km=total,
                annual_combined_tCO2e=activity[vehicle]*(m+e)/1000,
                ICEV_Peng2017_Table8_g_per_km=ice_intensity,
                relative_change_vs_ICEV_pct=(1-total/ice_intensity)*100,
                eligible_for_strict_comparison='YES' if eligible else 'NO_RETROSPECTIVE_METHOD_OR_GEOGRAPHY_CHANGE',
                status='TWO_STAGE_SCREENING' if eligible else 'RETROSPECTIVE_ELECTRICITY_FACTOR_TRANSFER'))
    write('R9_5_GRID_FACTOR_SENSITIVITY.csv',grid_sensitivity)

    factorial=[]
    for factor in strict:
        ef=num(factor['value'])
        for life in (150000,200000,250000):
            for vehicle in ('ICEV','BEV_NMC','BEV_LFP'):
                e=gas_kg_km if vehicle=='ICEV' else bev_kwh_km*ef
                m=manufacture[vehicle]/life
                factorial.append(dict(grid_scenario=factor['scenario_id'],grid_EF_kgCO2e_per_kWh=ef,
                    lifetime_km=life,vehicle=vehicle,manufacturing_gCO2e_per_km=m*1000,
                    energy_WTW_gCO2e_per_km=e*1000,two_stage_gCO2e_per_km=(m+e)*1000,
                    annual_two_stage_tCO2e=activity[vehicle]*(m+e)/1000,
                    status='STRICT_PRE_2023_WTW_SENSITIVITY'))
    write('R9_5_GRID_LIFETIME_FACTORIAL.csv',factorial)

    break_even=[]
    for life in (100000,150000,200000,250000,300000):
        ice=manufacture['ICEV']/life+gas_kg_km
        for vehicle in ('BEV_NMC','BEV_LFP'):
            threshold=(ice-manufacture[vehicle]/life)/bev_kwh_km
            break_even.append(dict(lifetime_km=life,vehicle=vehicle,
                break_even_grid_EF_kgCO2e_per_kWh=threshold,
                Peng2017_Table8_grid_EF_kgCO2e_per_kWh=default_ef,
                baseline_BE V_below_threshold='YES' if default_ef<threshold else 'NO',
                ICEV_gCO2e_per_km=ice*1000,
                BEV_at_break_even_equals_ICEV_gCO2e_per_km=ice*1000,
                formula='(ICEV_manufacturing_per_km + gasoline_WTW_per_km - BEV_manufacturing_per_km) / BEV_kWh_per_km'))
    write('R9_5_BREAK_EVEN_GRID_FACTOR.csv',break_even)

    battery=[]
    capacities={'BEV':40.0,'PHEV':12.8}
    for factor in batteries:
        value=num(factor['value'])
        for life in (150000,200000):
            for vehicle in ('BEV','PHEV'):
                new_kwh=vkt[vehicle]/life*capacities[vehicle]
                annual_t=new_kwh*value/1000
                intensity=capacities[vehicle]*value/life*1000
                battery.append(dict(source_id=factor['scenario_id'],vehicle=vehicle,
                    pack_capacity_kWh=capacities[vehicle],battery_service_lifetime_km=life,
                    battery_factor_kgCO2e_per_kWh=value,factor_boundary=factor['boundary'],
                    annual_new_battery_capacity_kWh=new_kwh,
                    annual_battery_only_GWP_tCO2e=annual_t,
                    battery_only_gCO2e_per_vehicle_km=intensity,
                    add_to_Qiao_vehicle_manufacturing='NO',
                    eligibility=factor['eligibility'],
                    note='PHEV chemistry is unverified; battery-only module; no replacement within assumed service life'))
    write('R9_5_BATTERY_FACTOR_SENSITIVITY.csv',battery)

    retrospective=[]
    for factor in grids:
        ef=num(factor['value'])
        if factor['scope']=='electricity_lifecycle_PCF':
            e=bev_kwh_km*ef
            total=(manufacture['BEV_NMC']/200000+e)*1000
            retrospective.append(dict(scenario=factor['scenario_id'],scope=factor['scope'],
                geography=factor['geography'],factor_kg_per_kWh=ef,
                BEV_grid_component_gCO2e_per_km=e*1000,
                BEV_manufacture_plus_grid_PCF_gCO2e_per_km=total,
                BEV_annual_electricity_component_tCO2e=vkt['BEV']*e/1000,
                comparison_warning='National electricity PCF factor is post-competition and not Beijing-specific; fuel factor remains Peng2017, so this is a mixed-vintage transfer'))
        elif factor['scope']=='generation_only_CO2':
            e=bev_kwh_km*ef
            retrospective.append(dict(scenario=factor['scenario_id'],scope=factor['scope'],
                geography=factor['geography'],factor_kg_per_kWh=ef,
                BEV_grid_component_gCO2e_per_km=e*1000,
                BEV_manufacture_plus_grid_PCF_gCO2e_per_km='NA',
                BEV_annual_electricity_component_tCO2e=vkt['BEV']*e/1000,
                comparison_warning='Generation-only CO2; not WTW and not CO2e; do not combine with Qiao/Peng two-stage GWP'))
    write('R9_5_RETROSPECTIVE_GRID_CROSSCHECK.csv',retrospective)

    tests=[]
    def ck(name,actual,expected,tol=1e-6,note=''):
        ok=close(actual,expected,tol)
        tests.append(dict(test=name,actual=actual,expected=expected,tolerance=tol,
                          status='PASS' if ok else 'FAIL',note=note))
        if not ok: raise AssertionError(name+': '+str(actual)+' != '+str(expected))
    ck('ICEV_baseline_R9_4_g_per_km',ice_intensity,265.537727,.001)
    bevbase=next(x for x in lifetime if x['vehicle']=='BEV_NMC' and x['lifetime_km']==200000)
    ck('BEV_NMC_baseline_R9_4_g_per_km',bevbase['two_stage_gCO2e_per_km'],186.32548,.001)
    lfpbase=next(x for x in lifetime if x['vehicle']=='BEV_LFP' and x['lifetime_km']==200000)
    ck('BEV_LFP_baseline_R9_4_g_per_km',lfpbase['two_stage_gCO2e_per_km'],187.17048,.001)
    ck('BEV_kWh_per_km',bev_kwh_km,.152,1e-9)
    ck('ICEV_gasoline_L_per_km',gas_l_km,.075,1e-9)
    ck('Peng_Table8_kWh_factor',default_ef,.73224,1e-9)
    ck('Peng_text_alt_kWh_factor',num(next(x for x in grids if x['scenario_id']=='Peng2017_text_WTW')['value']),.6048,1e-9)
    ck('BEV_NMC_baseline_annual_t',bevbase['annual_two_stage_tCO2e'],79612.33684744925,.01)
    ck('ICEV_baseline_annual_t',next(x for x in lifetime if x['vehicle']=='ICEV' and x['lifetime_km']==200000)['annual_two_stage_tCO2e'],520850.16540296585,.01)
    ck('break_even_baseline_NMC',next(x for x in break_even if x['vehicle']=='BEV_NMC' and x['lifetime_km']==200000)['break_even_grid_EF_kgCO2e_per_kWh'],1.2533732039473684,1e-8)
    ck('Sun2020_battery_base_150k',next(x for x in battery if x['source_id']=='Sun2020_NCM622' and x['vehicle']=='BEV' and x['battery_service_lifetime_km']==150000)['annual_battery_only_GWP_tCO2e'],14183.27211181993,.01)
    ck('Battery_factor_no_double_count',int(all(x['add_to_Qiao_vehicle_manufacturing']=='NO' for x in battery)),1)
    ck('MEE_grid_generation_scope_separate',int(next(x for x in retrospective if x['scenario']=='MEE2023_Beijing_CO2')['scope']=='generation_only_CO2'),1)
    ck('MEE2023_post_competition_flag',int(next(x for x in grids if x['scenario_id']=='MEE2023_national_PCF')['eligibility']=='RETROSPECTIVE_ONLY_POST_COMPETITION'),1)
    ck('Lifetime_monotonic_manufacturing',int(all(next(x for x in lifetime if x['vehicle']=='BEV_NMC' and x['lifetime_km']==a)['manufacturing_gCO2e_per_km'] > next(x for x in lifetime if x['vehicle']=='BEV_NMC' and x['lifetime_km']==b)['manufacturing_gCO2e_per_km'] for a,b in [(100000,150000),(150000,200000),(200000,250000),(250000,300000)])),1)
    ck('Battery_factor_rows',len(battery),44)
    ck('Lifetime_rows',len(lifetime),15)
    ck('Grid_lifetime_rows',len(factorial),18)
    ck('Break_even_rows',len(break_even),10)
    ck('Grid_sensitivity_rows',len(grid_sensitivity),6)
    ck('Retrospective_rows',len(retrospective),2)
    ck('No_full_LCA_claim',int(all(x['status']=='TWO_STAGE_SCREENING_NOT_FULL_LCA' for x in lifetime)),1)
    write('R9_5_TESTS.csv',tests)
    summary=[
      dict(metric='ICEV_two_stage_GWP100',value=ice_intensity,unit='gCO2e/vehicle-km',scenario='Peng2017_Table8 + Qiao2017, 200000 km'),
      dict(metric='BEV_NMC_two_stage_GWP100',value=bevbase['two_stage_gCO2e_per_km'],unit='gCO2e/vehicle-km',scenario='Peng2017_Table8 + Qiao2017, 200000 km'),
      dict(metric='BEV_LFP_two_stage_GWP100',value=lfpbase['two_stage_gCO2e_per_km'],unit='gCO2e/vehicle-km',scenario='Peng2017_Table8 + Qiao2017, 200000 km'),
      dict(metric='BEV_NMC_reduction_vs_ICEV',value=(1-bevbase['two_stage_gCO2e_per_km']/ice_intensity)*100,unit='%',scenario='strict two-stage screening only'),
      dict(metric='BEV_NMC_break_even_grid_EF',value=next(x for x in break_even if x['vehicle']=='BEV_NMC' and x['lifetime_km']==200000)['break_even_grid_EF_kgCO2e_per_kWh'],unit='kgCO2e/kWh',scenario='equal vehicle lifetime 200000 km'),
    ]
    write('R9_5_SUMMARY.csv',summary)
    print('R9.5 complete:',len(tests),'checks PASS;',len(lifetime),'lifetime rows;',len(grid_sensitivity),'grid rows;',len(factorial),'factorial rows;',len(battery),'battery rows')
if __name__=='__main__':
    main()
