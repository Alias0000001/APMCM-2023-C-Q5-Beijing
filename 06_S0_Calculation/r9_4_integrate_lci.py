#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.4 gated integration of R9.1-R9.3 into non-overlapping lifecycle tracks.

Run from any directory: python 06_S0_Calculation/r9_4_integrate_lci.py
Requires repository CSVs from R7/R9.1/R9.2/R9.3, standard library only.
The script preserves three disjoint reporting domains:
  A. Yang2021 modelled PHYSICAL CO2/VOC/NOx/PM2.5/SO2 kg/year:
     partial private-car stages and selected bus diesel/BEV energy WTW.
  B. Peng2017 fuel WTW CO2e + Qiao2017 vehicle production CO2e:
     *two-stage* GWP100 screening only (no maintenance, EOL, etc.).
  C. Sun2020 ReCiPe battery-only characterization by impact category:
     not added to physical emissions nor Qiao manufacturing GWP.
All remaining unknown flows are NA; partial subtotals are not lower bounds.
"""
from collections import defaultdict
from pathlib import Path
import csv
import math

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"07_LCA_LCIA"
R7=ROOT/"02_Cleaned_Data"/"R7_S0_CO2_scenarios.csv"
POLLUTANTS=("CO2","VOC","NOx","PM2.5","SO2")
STAGES=("material_production_major_materials","parts_manufacturing",
        "vehicle_distribution","maintenance_replacements",
        "end_of_life_dismantling_energy","energy_supply_and_vehicle_use_WTW")
PASSENGER={"ICEV":"ice_vkt_km","BEV":"private_bev_vkt_km","PHEV":"phev_vkt_km"}
BUS_VKT_KEYS={"bus_diesel":"bus_diesel_vkt_km",
              "bus_assumed_BEV":"bus_bev_vkt_km_assumed",
              "bus_natural_gas":"bus_gas_vkt_km",
              "bus_unassigned_nonBEV":"bus_nonbev_mixed_vkt_km",
              "bus_unclassified":"bus_unknown_vkt_km"}
BUS_MAPPED={"diesel":"bus_diesel","electricity":"bus_assumed_BEV"}
CARRIERS={"ICEV":("gasoline",),"BEV":("electricity",),
          "PHEV":("gasoline","electricity")}
DENSITY={"gasoline":.74,"diesel":.84}
LHV={"gasoline":43.07,"diesel":42.652}
ELECTRICITY_MJ_PER_KWH=3.6

def read(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def numeric(v):
    try:
        n=float(v)
    except (TypeError,ValueError):
        return None
    return n if math.isfinite(n) else None

def save(name,rows):
    if not rows: raise ValueError("No rows for "+name)
    dest=D/name
    with dest.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def close(x,y,tol=1.e-7):
    return math.isclose(x,y,rel_tol=tol,abs_tol=tol)

def main():
    base=next(x for x in read(R7) if x["scenario"]=="S0_screening")
    vkt={k:float(base[key]) for k,key in {**PASSENGER,**BUS_VKT_KEYS}.items()}
    stage=read(D/"R9_LCI_PASSENGER_STAGE_EMISSIONS.csv")
    bus=read(D/"R9_LCI_BUS_USE_STAGE.csv")
    battery=read(D/"R9_3_NCM622_BATTERY_LCIA_SCENARIOS.csv")
    manufacturing=read(D/"R9_LCI_VEHICLE_MANUFACTURING_PROXY.csv")
    use=read(D/"R9_LCI_PASSENGER_USE_ENERGY.csv")
    peng=read(D/"R9_LCI_PARTIAL_WTW_GHG.csv")
    foreground=read(D/"R9_LCI_FOREGROUND_FLOWS.csv")
    checks=[]
    def check(name,result,expected,tol=1.e-7,reason=""):
        good=close(result,expected,tol)
        checks.append(dict(test=name,actual=result,expected=expected,
                           tolerance=tol,status="PASS" if good else "FAIL",note=reason))
        if not good: raise AssertionError(f"{name}: {result}!={expected}")

    check("R7_private_VKT_sum",sum(vkt[k] for k in PASSENGER),
          float(base["private_total_vkt_km"]),.001)
    check("R7_bus_VKT_sum",sum(vkt[k] for k in BUS_VKT_KEYS),
          float(base["bus_total_vkt_km"]),.001)
    assert len(stage)==3*len(STAGES)*len(POLLUTANTS),"Unexpected private-stage ledger length"
    assert {(x["vehicle"],x["stage"],x["pollutant"]) for x in stage} == {
        (k,s,p) for k in PASSENGER for s in STAGES for p in POLLUTANTS}
    assert all(x["unit"]=="kg/year" and numeric(x["annual_amount"]) is not None
               and numeric(x["annual_amount"])>=0 for x in stage)
    check("Yang2021_stage_records",len(stage),90)
    bbase=[x for x in bus if x["scenario"]=="R7_base_q0.8"]
    assert len(bbase)==5 and {x["carrier"] for x in bbase}=={
        "diesel","electricity","CNG_or_LNG","mixed_nonBEV_unallocated","unclassified_bus"}
    assert all(numeric(x["CO2_kg_per_year"]) is None for x in bbase
               if x["carrier"] not in BUS_MAPPED)
    d=next(x for x in bbase if x["carrier"]=="diesel")
    e=next(x for x in bbase if x["carrier"]=="electricity")
    check("R7_bus_diesel_liters",float(d["annual_amount"]),
          vkt["bus_diesel"]*35/100,.01)
    check("R7_bus_BEV_kWh",float(e["annual_amount"]),
          vkt["bus_assumed_BEV"]*.626,.01)
    useby={x["vehicle"]:x for x in use}
    assert set(useby)==set(PASSENGER)
    check("R7_private_fuel_liters",
          sum(float(x["gasoline_L"]) for x in use),
          next(float(x["amount"]) for x in foreground
               if x["flow_id"]=="EN-GAS-TOTAL"),.01)
    check("R7_total_electricity_kWh",
          sum(float(x["electricity_kWh"]) for x in use)+float(e["annual_amount"]),
          float(base["electric_kwh"]),.01)

    # Domain A: physical elementary flows from Yang2021 / selected bus WTW.
    phys=[]
    for x in stage:
        veh=x["vehicle"]; pol=x["pollutant"]; raw=float(x["annual_amount"])
        phys.append(dict(track="A_physical_mass",vehicle=veh,
            stage=x["stage"],flow=pol,unit="kg/year",
            annual_quantity=raw,source_id=x["source_id"],
            status=x["status"],included_in_known_subtotal="YES",
            scenario="2018_China_energy_and_reference_car_proxy",
            full_lifecycle_total_allowed="NO",
            note="Physical mass inventory proxy; manufacture and use based on different available sub-stages"))
    for x in bbase:
        veh=BUS_MAPPED.get(x["carrier"])
        for p in POLLUTANTS:
            if veh is None:
                key={"CNG_or_LNG":"bus_natural_gas",
                     "mixed_nonBEV_unallocated":"bus_unassigned_nonBEV",
                     "unclassified_bus":"bus_unclassified"}[x["carrier"]]
                phys.append(dict(track="A_physical_mass",vehicle=key,
                    stage="energy_supply_and_vehicle_use_WTW",flow=p,unit="kg/year",
                    annual_quantity="NA",source_id="R9_LCI_BUS_USE_STAGE.csv",
                    status="MISSING_WTW_ENERGY_OR_POWERTRAIN",
                    included_in_known_subtotal="NO",
                    scenario="2018_China_energy_proxy_with_2023_R7_VKT",
                    full_lifecycle_total_allowed="NO",
                    note="Do not treat missing as zero; CNG/LNG and unassigned mixed propulsion unresolved"))
            else:
                n=numeric(x[p+"_kg_per_year"])
                if n is None:raise AssertionError("Missing assigned bus physical flow")
                phys.append(dict(track="A_physical_mass",vehicle=veh,
                    stage="energy_supply_and_vehicle_use_WTW",flow=p,unit="kg/year",
                    annual_quantity=n,source_id="Yang2021_Table6 + R7_bus_VKT",
                    status="PARTIAL_2018_ENERGY_FACTOR_2023_ACTIVITY",
                    included_in_known_subtotal="YES",
                    scenario="R7_q0.8_2018_China_energy_proxy",
                    full_lifecycle_total_allowed="NO",
                    note="Diesel/assigned BEV bus WTW only; all other bus stages NA"))
    check("PHYSICAL_CORE_RECORDS",len(phys),115)

    stage_sum=defaultdict(float)
    physical_sum=defaultdict(float)
    for x in phys:
        n=numeric(x["annual_quantity"])
        if n is None:continue
        k=(x["vehicle"],x["stage"],x["flow"])
        stage_sum[k]+=n
        physical_sum[(x["vehicle"],x["flow"])]+=n
    stage_output=[dict(track="A_physical_mass",vehicle=v,stage=s,flow=f,
        annual_known_kg=value,unit="kg/year",
        status="PARTIAL_STAGE_SUM_NA_COMPONENTS_EXIST",annual_VKT_km=vkt[v],
        kg_per_vehicle_km=value/vkt[v],
        full_lifecycle_total_allowed="NO")
        for (v,s,f),value in sorted(stage_sum.items())]
    physical_output=[]
    for v in (*PASSENGER,*BUS_VKT_KEYS):
        for p in POLLUTANTS:
            key=(v,p);has=key in physical_sum
            physical_output.append(dict(track="A_physical_mass",vehicle=v,flow=p,
                annual_known_kg=physical_sum[key] if has else "NA",
                kg_per_vehicle_km=physical_sum[key]/vkt[v] if has else "NA",
                annual_VKT_km=vkt[v],unit="kg/year",
                status=("PARTIAL_KNOWN_FLOW_SUBTOTAL_NOT_FULL_LCA" if has
                        else "MISSING_NO_SUBTOTAL"),
                allowed_to_rank_full_lifecycle="NO",
                note="Known-flow subtotal is not a mathematical lower bound; recycling credits and negative flows may arise"))
    # Domain B: 2-stage CO2e screening with mutually exclusive Peng/Qiao data.
    man={(x["vehicle_class"]):x for x in manufacturing}
    factors={}
    for x in peng:
        if x["carrier"] not in ("gasoline","diesel","electricity"):
            continue
        if x["factor_scenario"]=="TLCAM_2017_Table_8":
            factors[("table8",x["carrier"])]=float(x["WTW_factor_gCO2e_MJ"])
        elif x["factor_scenario"]=="TLCAM_2017_text_alternative":
            factors[("text",x["carrier"])]=float(x["WTW_factor_gCO2e_MJ"])
    for f in ("gasoline","diesel","electricity"):
        assert ("table8",f) in factors and ("text",f) in factors
    def wtw_t(vehicle,flavor):
        if vehicle in PASSENGER:
            x=useby[vehicle]
            mj=factors[(flavor,"gasoline")]*float(x["gasoline_L"])*DENSITY["gasoline"]*LHV["gasoline"]
            mj+=factors[(flavor,"electricity")]*float(x["electricity_kWh"])*ELECTRICITY_MJ_PER_KWH
            return mj/1e6
        if vehicle=="bus_diesel":
            return float(d["annual_amount"])*DENSITY["diesel"]*LHV["diesel"]*factors[(flavor,"diesel")]/1e6
        if vehicle=="bus_assumed_BEV":
            return float(e["annual_amount"])*ELECTRICITY_MJ_PER_KWH*factors[(flavor,"electricity")]/1e6
        return None
    screening=[]
    classes=[
      ("ICEV","private_ICEV","ICEV"),
      ("BEV_NMC","private_BEV_NMC","BEV"),
      ("BEV_LFP","private_BEV_LFP","BEV"),
      ("PHEV","private_PHEV","PHEV"),
      ("bus_diesel","bus_diesel","bus_diesel"),
      ("bus_assumed_BEV","bus_BEV","bus_assumed_BEV"),
    ]
    for flavor in ("table8","text"):
        for label,mf,activity in classes:
            assert mf in man
            row=man[mf]
            manuf=numeric(row["annualized_manufacturing_tCO2e"])
            energy=wtw_t(activity,flavor)
            complete_two_stage=manuf is not None and energy is not None
            total=manuf+energy if complete_two_stage else None
            screening.append(dict(track="B_two_stage_GWP100_CO2e",
                scenario="Peng2017_Table8_default" if flavor=="table8" else
                         "Peng2017_text_alternative_2015_grid",
                vehicle=label,annual_VKT_km=vkt[activity],
                cradle_to_gate_vehicle_manufacturing_tCO2e=manuf if manuf is not None else "NA",
                fuel_and_electricity_WTW_tCO2e=energy if energy is not None else "NA",
                known_two_stage_GWP_tCO2e=total if total is not None else "NA",
                known_two_stage_GWP_gCO2e_per_km=total*1e6/vkt[activity]
                   if total is not None else "NA",
                manufacturing_lifetime_km=200000 if manuf is not None else "NA",
                status="TWO_STAGE_SCREENING_NOT_FULL_CRADLE_TO_GRAVE" if complete_two_stage
                       else "INCOMPLETE_MANUFACTURING_NA",
                units="tCO2e/year; gCO2e/vehicle-km",
                prohibition="DO_NOT_ADD_R7_CO2_OR_SUN_BATTERY_GWP_OR_YANG_PHYSICAL_CO2"))
    check("TWO_STAGE_SCREENING_RECORDS",len(screening),12)

    # Domain C: whole Sun2020 battery module only, no mixing with A/B.
    lcia=[]
    cats=set()
    for x in battery:
        v=x["vehicle"]
        assert v in ("BEV","PHEV")
        impact=float(x["sum_annual"])
        vkt_this=vkt[v]
        assert close(float(x["annual_vkt_km"]),vkt_this)
        cats.add(x["impact_category"])
        lcia.append(dict(track="C_battery_ReCiPe_only",
             vehicle=v,scenario=x["scenario"],impact_category=x["impact_category"],
             annual_characterized_amount=impact,
             characterized_per_vehicle_km=impact/vkt_this,
             unit=x["impact_unit"],annual_VKT_km=vkt_this,
             source_id=x["source_id"],status="BATTERY_ONLY_LCIA",
             summable_with_physical_mass="NO",
             summable_with_Qiao_vehicle_GWP="NO",
             note="Published ReCiPe factors use source's characterization; no 2023 local chemistry observation"))
    check("SUN_RECIPE_INDICATOR_COUNT",len(cats),11)
    check("SUN_BATTERY_CHARACTERIZED_RECORDS",len(lcia),44)

    # Coverage: vehicle x relevant stages. No blank disguised as zero.
    phases=(
      "vehicle_materials", "parts_manufacturing", "vehicle_distribution",
      "vehicle_assembly", "battery_manufacturing", "energy_WTW",
      "maintenance", "end_of_life_dismantling", "end_of_life_recycling",
      "non_exhaust", "passenger_km")
    coverage=[]
    all_classes=(*PASSENGER,*BUS_VKT_KEYS)
    for vehicle in all_classes:
        for phase in phases:
            if vehicle in PASSENGER:
                if phase in ("vehicle_materials","parts_manufacturing",
                             "vehicle_distribution","maintenance",
                             "end_of_life_dismantling","energy_WTW"):
                    grade="PARTIAL_PHYSICAL";source="Yang2021"
                elif phase=="battery_manufacturing":
                    grade="SEPARATE_LCIA_ONLY" if vehicle in ("BEV","PHEV") else "NOT_APPLICABLE_TRACTION_BATTERY"
                    source="Sun2020" if vehicle in ("BEV","PHEV") else "NA"
                else:grade="MISSING";source="NA"
            else:
                if phase=="energy_WTW" and vehicle in ("bus_diesel","bus_assumed_BEV"):
                    grade="PARTIAL_PHYSICAL";source="Yang2021_Table6 + R7"
                else:
                    grade="MISSING";source="NA"
            coverage.append(dict(vehicle=vehicle,stage=phase,
                annual_VKT_km=vkt[vehicle],coverage_status=grade,
                source_id=source,
                is_2023_direct_observation="NO",
                fully_modelled_cradle_to_grave="NO",
                note="2015 Lin bus material shares and PKM only historical alternatives; 2023 matched inputs unavailable"))
    check("COVERAGE_MATRIX_RECORDS",len(coverage),8*len(phases))

    # Bridge diagnostics and unsupported downstream interpretation guards.
    known_bus_vkt=vkt["bus_diesel"]+vkt["bus_assumed_BEV"]
    check("R7_bus_WTW_quantified_VKT_le_total",int(known_bus_vkt<=float(base["bus_total_vkt_km"])),1)
    check("Sun2020_GWP_BEV_CTG",float(next(x["sum_annual"] for x in battery
          if x["vehicle"]=="BEV" and x["scenario"]=="cradle_to_gate_no_recycling_credit"
          and x["impact_category"]=="GWP100")),113940.16799341203*124.48,.1)
    check("Sun2020_GWP_BEV_100pct_recycling",float(next(x["sum_annual"] for x in battery
          if x["vehicle"]=="BEV" and x["scenario"]=="hypothetical_100pct_hydromet_recycling"
          and x["impact_category"]=="GWP100")),113940.16799341203*93.57,.1)
    check("Physical_CO2_ICEV_WTW",float(next(x["annual_amount"] for x in stage
          if x["vehicle"]=="ICEV" and x["stage"]=="energy_supply_and_vehicle_use_WTW"
          and x["pollutant"]=="CO2")),411200866.62626135,.1)
    assert all(x["full_lifecycle_total_allowed"]=="NO" for x in phys)
    assert all(x["summable_with_physical_mass"]=="NO" for x in lcia)
    assert all(x["allowed_to_rank_full_lifecycle"]=="NO" for x in physical_output)
    assert all(x["known_two_stage_GWP_tCO2e"]=="NA"
               for x in screening if x["vehicle"] in
               ("PHEV","bus_diesel","bus_assumed_BEV"))

    save("R9_4_PHYSICAL_FLOW_LEDGER.csv",phys)
    save("R9_4_PHYSICAL_STAGE_SUBTOTALS.csv",stage_output)
    save("R9_4_PHYSICAL_VEHICLE_PARTIAL_SUBTOTALS.csv",physical_output)
    save("R9_4_TWO_STAGE_GWP100_SCREENING.csv",screening)
    save("R9_4_BATTERY_RECIPE_ONLY.csv",lcia)
    save("R9_4_STAGE_COVERAGE_MATRIX.csv",coverage)
    checks.append(dict(test="A_and_B_and_C_domain_separation",actual=1,expected=1,
                       tolerance=0,status="PASS",
                       note="No code path sums physical kgCO2 with GWP kgCO2e or Sun ReCiPe impacts"))
    checks.append(dict(test="no_citywide_full_LCA_reported",actual=1,expected=1,
                       tolerance=0,status="PASS",
                       note="Citywide all-vehicle manufacturing and energy flows unresolved"))
    save("R9_4_INTEGRATION_TESTS.csv",checks)

    def val(v,s,f):
        return next(x for x in screening if x["vehicle"]==v
                    and x["scenario"]==s)[f]
    print("R9.4 integrated A physical kg/year, B two-stage GWP100, C battery ReCiPe")
    print("Physical modeled flow rows:",len(phys))
    print("Bus WTW quantified VKT share: {:.3%}".format(
          known_bus_vkt/float(base["bus_total_vkt_km"])))
    print("Two-stage CO2e default ICEV (t):",val("ICEV","Peng2017_Table8_default","known_two_stage_GWP_tCO2e"))
    print("Two-stage CO2e default BEV NMC (t):",val("BEV_NMC","Peng2017_Table8_default","known_two_stage_GWP_tCO2e"))
    print("All lifecycle totals remain incomplete.")
    print("Checks:",len(checks),"PASS")
if __name__=="__main__":
    main()
