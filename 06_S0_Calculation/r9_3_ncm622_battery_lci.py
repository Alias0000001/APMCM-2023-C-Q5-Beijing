#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.3: NCM622 cradle-to-gate battery LCI plus hypothetical recycling.

Reference: Sun et al. (2020), Journal of Cleaner Production 273, 123006,
Cambridge accepted PDF including SI Tables S2/S3/S5/S6 and main Tables 1/2.
Read R7 S0 annual VKT only for scaling, with 150000-km vehicle lifetime.
Not observed Beijing battery chemistry or pack capacity.
Run at repository root:
    python 06_S0_Calculation/r9_3_ncm622_battery_lci.py

Outputs: modelled annual physical flows, nested cathode inputs, LCIA
characterized indicators (not measured pollutant emissions), and audits.
No credit is the cradle-to-gate case, NOT complete cradle-to-grave.
Full credit assumes 100% collection + hydrometallurgical recycling.
"""
from pathlib import Path
from collections import defaultdict
import csv

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"07_LCA_LCIA"
R7=ROOT/"02_Cleaned_Data"/"R7_S0_CO2_scenarios.csv"
SOURCE="SUN2020_NCM622"
LIFETIME_VKT=150000.0
REFERENCE_PACK_KWH=72.5
REFERENCE_PACK_KG=630.0
PACKS={
    "BEV":("private_bev_vkt_km",40.0,286.0,
           "C_BEV_NCM622_capacity_transfer_Yang2021_mass_not_matched"),
    "PHEV":("phev_vkt_km",12.8,128.0,
            "D_PHEV_NCM622_exploratory_chemistry_not_verified"),
}
SCENARIOS={
    "cradle_to_gate_no_recycling_credit":0.0,
    "hypothetical_100pct_hydromet_recycling":1.0,
}

def load(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def emit(path,rows):
    if not rows: raise ValueError("Missing output rows: "+str(path))
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def close(a,b,tol=1e-6):
    return abs(a-b)<=tol

def main():
    base=next(r for r in load(R7) if r["scenario"]=="S0_screening")
    bom=load(D/"R9_3_NCM622_PACK_BOM.csv")
    upstream=load(D/"R9_3_NCM622_CATHODE_UPSTREAM.csv")
    factory=load(D/"R9_3_NCM622_FACTORY_PROCESS.csv")
    recycle=load(D/"R9_3_NCM622_RECYCLING_PROCESS.csv")
    impacts=load(D/"R9_3_NCM622_LCIA_FACTORS.csv")

    checks=[]
    def check(name, actual, expected, tol=1e-6, note=""):
        status="PASS" if close(actual,expected,tol) else "FAIL"
        checks.append(dict(check_id=name,actual=actual,expected=expected,
                           tolerance=tol,status=status,note=note))
        if status!="PASS": raise AssertionError(name+" "+str(actual))
    check("BOM_rounded_mass_kg",sum(float(r["kg_per_72_5kWh_reference_pack"])
          for r in bom),629.8,0.01,"630 kg stated total; 0.2 kg table rounding difference")
    check("S6_factory_electricity_MJ_per_kWh",
          sum(float(r["quantity_per_kWh"]) for r in factory
              if r["flow_id"]=="electricity" and r["process"]!="initial_charging"),
          72.0)
    check("S6_factory_steam_MJ_per_kWh",
          sum(float(r["quantity_per_kWh"]) for r in factory
              if r["flow_id"]=="steam"),34.0)
    check("initial_charge_MJ_per_kWh",
          sum(float(r["quantity_per_kWh"]) for r in factory
              if r["process"]=="initial_charging"),4.0)
    check("factory_electricity_steam_initial_charge_MJ_per_kWh",
          72.0+34.0+4.0,110.0)
    for r in impacts:
        subtotal=sum(float(r[k]) for k in
           ("material_stage_per_kWh","production_stage_per_kWh","EOL_credit_per_kWh"))
        published=float(r["source_reported_total_per_kWh"])
        check("ReCiPe_"+r["indicator_id"],subtotal,published,.021,
              "Source Table2 values rounded to 2 decimals; impacts not raw emissions")
    # Independent activities must reconcile to R7.
    private_total=sum(float(base[x]) for x in
        ("ice_vkt_km","private_bev_vkt_km","phev_vkt_km"))
    check("R7_private_activity_reconciliation",private_total,
          float(base["private_total_vkt_km"]),.0001)

    # Source BOM is 629.8kg/72.5kWh; capacity-scaling is a scenario.
    physical=[]
    nested=[]
    results=[]
    audit=[]
    precursor_name="ncm622_cathode_active"
    cathode_mass_kg_per_kwh=next(float(r["kg_per_kWh"])
        for r in bom if r["material_id"]==precursor_name)
    for vehicle,(vkt_field,capacity,mass_yang,quality) in PACKS.items():
        annual_vkt=float(base[vkt_field])
        vehicles_equiv=annual_vkt/LIFETIME_VKT
        annual_kwh=capacity*vehicles_equiv
        pack_mass_kg=capacity*629.8/72.5
        mass_diff_pct=100*(pack_mass_kg/mass_yang-1)
        audit.append(dict(vehicle=vehicle,annual_VKT_km=annual_vkt,
            lifetime_VKT_km=LIFETIME_VKT,annual_vehicle_equiv=vehicles_equiv,
            assumed_capacity_kWh_per_vehicle=capacity,
            annual_new_battery_capacity_kWh=annual_kwh,
            Sun2020_implied_pack_mass_kg=pack_mass_kg,
            Yang2021_reference_battery_mass_kg=mass_yang,
            mass_mismatch_percent=mass_diff_pct,
            grade_and_scope=quality,
            status="SOURCE_MISMATCH_SEPARATE_BATTERY_MODULE_DO_NOT_ADD_BOM_TO_YANG_TOTAL"))

        for r in bom:
            physical.append(dict(vehicle=vehicle,scenario="new_pack_manufacturing",
                stage="battery_material_BOM",flow=r["material_id"],
                annual_quantity=annual_kwh*float(r["kg_per_kWh"]),
                unit="kg/year",source_id=SOURCE,flow_role="reference_pack_material_intake",
                caveat="Separate battery BOM; not additive to Yang2021 embedded battery mass"))
        for r in factory:
            amount=float(r["quantity_per_kWh"])*annual_kwh
            physical.append(dict(vehicle=vehicle,scenario="new_pack_manufacturing",
                stage=r["process"],flow=r["flow_id"],annual_quantity=amount,
                unit=r["unit"]+"/year",source_id=SOURCE,
                flow_role=r["flow_role"],
                caveat="4 MJ initial charge separate; energy flows not additional to published production GWP"))
        # Nested cathode production flows are intermediary, not independent final-product BOM.
        ncm_total=annual_kwh*cathode_mass_kg_per_kwh
        for r in upstream:
            nested.append(dict(vehicle=vehicle,step=r["process"],
                input_flow=r["flow_id"],annual_quantity=ncm_total*
                float(r["quantity_per_kg_product"]),
                unit=r["unit"]+"/year",source_id=SOURCE,
                status="NESTED_PRECURSOR_CHAIN_NOT_ADDITIVE_TO_FINAL_BOM",
                note="NCM622 cathode active mass multiplied by S2/S3 process inputs; do not add precursor twice"))

        for scen,share in SCENARIOS.items():
            if share:
                for r in recycle:
                    if r["flow_id"]=="spent_NCM622_battery":continue
                    physical.append(dict(vehicle=vehicle,scenario=scen,
                        stage="hydromet_recycling_"+r["flow_group"],
                        flow=r["flow_id"],
                        annual_quantity=annual_kwh*float(r["quantity_per_kWh_recycled"])*share,
                        unit=r["unit"]+"/year",source_id=SOURCE,
                        flow_role="recycling_process_physical_flow_OR_recovered_material",
                        caveat="100pct battery collection assumed; recovered output not automatically netted against new BOM"))
            for r in impacts:
                m=annual_kwh*float(r["material_stage_per_kWh"])
                p=annual_kwh*float(r["production_stage_per_kWh"])
                e=annual_kwh*float(r["EOL_credit_per_kWh"])*share
                results.append(dict(vehicle=vehicle,scenario=scen,
                    quality_grade=quality,annual_vkt_km=annual_vkt,
                    annual_equivalent_vehicles=vehicles_equiv,
                    reference_lifetime_VKT_km=LIFETIME_VKT,
                    pack_capacity_kWh_per_vehicle=capacity,
                    annual_new_battery_capacity_kWh=annual_kwh,
                    recycling_fraction_assumed=share,
                    impact_category=r["indicator_id"],
                    impact_unit=r["unit"]+"/year",
                    material_stage_annual=m,production_stage_annual=p,
                    end_of_life_net_credit_annual=e,
                    sum_annual=m+p+e,source_id=SOURCE,
                    result_type=("PARTIAL_CRADLE_TO_GATE_NO_EOL" if not share
                                 else "HYPOTHETICAL_100PCT_RECYCLING_NO_BATTERY_USE")))
            check(vehicle+"_annual_pack_capacity",annual_kwh,
                  annual_vkt/LIFETIME_VKT*capacity)
    emit(D/"R9_3_NCM622_BATTERY_ANNUAL_FOREGROUND.csv",physical)
    emit(D/"R9_3_NCM622_CATHODE_NESTED_ANNUAL.csv",nested)
    emit(D/"R9_3_NCM622_BATTERY_LCIA_SCENARIOS.csv",results)
    emit(D/"R9_3_NCM622_CAPACITY_AND_MASS_AUDIT.csv",audit)
    emit(D/"R9_3_NCM622_BALANCE_CHECKS.csv",checks)
    print("R9.3 NCM622 battery model: 2 vehicle cases x 2 allocation cases x",
          len(impacts),"impact indicators")
    for r in results:
        if r["impact_category"]=="GWP100":
            print(r["vehicle"],r["scenario"],round(r["sum_annual"]/1000,2),
                  "tonnes CO2e/year; NOT complete vehicle LCA")
if __name__=="__main__":
    main()
