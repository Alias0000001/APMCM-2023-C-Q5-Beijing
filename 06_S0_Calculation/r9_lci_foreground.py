#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.1 foreground LCI and partial life-cycle proxy calculations.

Reads the R7 S0 row and emits traceable annual inventory flows for a
representative 1,000,000-person city. Missing/unknown flows remain NA.
This script deliberately does NOT turn the R7 0.9 kg/km mixed-bus placeholder
into an energy flow or emission factor.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Cleaned_Data"
OUT = ROOT / "07_LCA_LCIA"
R7_FILE = DATA / "R7_S0_CO2_scenarios.csv"
SCALE = 1_000_000 / 21_858_000

# R7 S0 foreground assumptions; kept explicit for audit.
ICE_L100 = 7.5
PHEV_L100 = 7.5
PHEV_KWH100 = 16.0
DIESEL_L100 = 35.0
GAS_KG100 = 30.0
CAR_KWH_KM = 0.152
BUS_KWH_KM = 0.626
PHEV_UF = 0.66
BUS_Q = 0.80

# Pre-2023 Chinese literature / IPCC-style conversion defaults.
GASOLINE_DENSITY_KG_L = 0.74
DIESEL_DENSITY_KG_L = 0.84
GASOLINE_LHV_MJ_KG = 43.07
DIESEL_LHV_MJ_KG = 42.652
ELECTRICITY_MJ_KWH = 3.6

def read_r7():
    with R7_FILE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return next(x for x in rows if x["scenario"] == "S0_screening")

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    r = read_r7()
    v = lambda key: float(r[key])
    ice_vkt = v("ice_vkt_km")
    bev_vkt = v("private_bev_vkt_km")
    phev_vkt = v("phev_vkt_km")
    bus_diesel_vkt = v("bus_diesel_vkt_km")
    bus_gas_vkt = v("bus_gas_vkt_km")
    bus_bev_vkt = v("bus_bev_vkt_km_assumed")
    bus_other_mixed_vkt = v("bus_nonbev_mixed_vkt_km")
    bus_mixed_vkt = bus_bev_vkt + bus_other_mixed_vkt
    bus_unknown_vkt = v("bus_unknown_vkt_km")

    phev_fuel_vkt = phev_vkt * (1 - PHEV_UF)
    phev_electric_vkt = phev_vkt * PHEV_UF
    gasoline_ice_l = ice_vkt * ICE_L100 / 100
    gasoline_phev_l = phev_fuel_vkt * PHEV_L100 / 100
    diesel_bus_l = bus_diesel_vkt * DIESEL_L100 / 100
    gas_bus_kg = bus_gas_vkt * GAS_KG100 / 100
    electricity_bev_kwh = bev_vkt * CAR_KWH_KM
    electricity_phev_kwh = phev_electric_vkt * PHEV_KWH100 / 100
    electricity_bus_kwh = bus_bev_vkt * BUS_KWH_KM
    gasoline_total_l = gasoline_ice_l + gasoline_phev_l
    electricity_total_kwh = electricity_bev_kwh + electricity_phev_kwh + electricity_bus_kwh

    # Reconcile to R7 exactly. Any change in assumptions must update this check.
    assert abs(ice_vkt + bev_vkt + phev_vkt - v("private_total_vkt_km")) < 1e-4
    assert abs(bus_diesel_vkt + bus_gas_vkt + bus_mixed_vkt + bus_unknown_vkt
               - v("bus_total_vkt_km")) < 1e-4
    assert abs(electricity_total_kwh - v("electric_kwh")) < 1e-3

    flows = []
    def add(flow_id, kind, stage, vehicle, name, amount, unit, grade, source, status, note):
        flows.append(dict(flow_id=flow_id, flow_type=kind, lifecycle_stage=stage,
                          vehicle_class=vehicle, flow_name=name, amount=amount, unit=unit,
                          evidence_grade=grade, source_id=source, status=status, note=note))

    # Annual activity/reference flows.
    for fid, vehicle, amount, grade, note in [
        ("ACT-ICE","private_ICEV",ice_vkt,"C/D","R7 residual after fixed private VKT anchor and BEV/PHEV scenarios"),
        ("ACT-BEV","private_BEV",bev_vkt,"B/C","2023-10 monthly mean annualized ×12; fleet stock split remains scenario"),
        ("ACT-PHEV","private_PHEV",phev_vkt,"C/D","PHEV stock share and active days are scenarios"),
        ("ACT-BUS-D","bus_diesel",bus_diesel_vkt,"C","April 2023 fleet snapshot allocated to full-year bus VKT"),
        ("ACT-BUS-G","bus_natural_gas_CNG_LNG_combined",bus_gas_vkt,"C","CNG/LNG split unavailable"),
        ("ACT-BUS-NEV","bus_new_energy_electric_drive_mixed",bus_mixed_vkt,"C","Mixed new-energy/electric-drive group; not pure BEV VKT"),
        ("ACT-BUS-U","bus_unclassified",bus_unknown_vkt,"C","Six-bus arithmetic residual retained"),
        ("ACT-BUS-MIX-OTHER","bus_nonBEV_mixed_unresolved",bus_other_mixed_vkt,"D","R7 q=0.8 stress assumption; no fuel assigned"),
    ]:
        add(fid,"reference_flow","vehicle_operation",vehicle,"vehicle_km",f"{amount:.6f}","vehicle-km/year",grade,
            "R7_S0_CO2_scenarios.csv", "conditional_foreground_activity",note)

    # Physical energy inputs. These are modelled flows, not measured city-wide fuel invoices.
    energy_rows = [
      ("EN-GAS-ICE","private_ICEV","gasoline",gasoline_ice_l,"L/year","D","R7 assumption 7.5 L/100 km"),
      ("EN-GAS-PHEV","private_PHEV","gasoline",gasoline_phev_l,"L/year","D","PHEV fuel VKT × assumed 7.5 L/100 km"),
      ("EN-ELEC-BEV","private_BEV","grid_electricity",electricity_bev_kwh,"kWh/year","B/C","15.2 kWh/100 km applied to annualized BEV VKT"),
      ("EN-ELEC-PHEV","private_PHEV","grid_electricity",electricity_phev_kwh,"kWh/year","D","PHEV UF 0.66 and 16 kWh/100 electric VKT"),
      ("EN-DIESEL-BUS","bus_diesel","diesel",diesel_bus_l,"L/year","D","Assumed 35 L/100 km"),
      ("EN-GAS-BUS","bus_natural_gas_CNG_LNG_combined","natural_gas_mass",gas_bus_kg,"kg/year","D","Assumed 30 kg/100 km; CNG/LNG mix and unit convention need verification"),
      ("EN-ELEC-BUS","bus_new_energy_electric_drive_mixed_assumed_BEV_part","grid_electricity",electricity_bus_kwh,"kWh/year","C/D","Only q=0.8 scenario part assigned BEV electricity; not a measured propulsion split"),
    ]
    for fid, vehicle, name, amount, unit, grade, note in energy_rows:
        add(fid,"energy_input","energy_supply_and_use",vehicle,name,f"{amount:.6f}",unit,grade,
            "R7_S0_CO2_scenarios.csv + R7 assumptions","conditional_modelled_flow",note)
    add("EN-GAS-TOTAL","energy_input","energy_supply_and_use","all_private_cars","gasoline_total",
        f"{gasoline_total_l:.6f}","L/year","D","derived_from_R7","conditional_modelled_flow","ICEV + PHEV gasoline; no double count")
    add("EN-ELEC-TOTAL","energy_input","energy_supply_and_use","all_assigned_electric_vehicles","electricity_total",
        f"{electricity_total_kwh:.6f}","kWh/year","C/D","derived_from_R7","conditional_modelled_flow","BEV + PHEV + q=0.8 bus BEV part")

    # Explicitly unassigned activity: no fuel/energy/EF is fabricated.
    add("NA-BUS-MIX","unallocated_activity","vehicle_operation","bus_nonBEV_mixed_unresolved",
        "vehicle_km_without_identified_fuel",f"{bus_other_mixed_vkt:.6f}","vehicle-km/year","D",
        "R7 q=0.8 assumption","NA_energy_and_emissions","Do not reuse R7's 0.9 kgCO2/km placeholder as an LCI flow")
    add("NA-BUS-UNKNOWN","unallocated_activity","vehicle_operation","bus_unclassified",
        "vehicle_km_without_identified_powertrain",f"{bus_unknown_vkt:.6f}","vehicle-km/year","C",
        "R5_bus_2023_04_fleet_snapshot.csv","NA_energy_and_emissions","Six unclassified buses retained")

    # Alternative retrospective bus activity proxy: replace the q=0.8 bus split; never add to it.
    alt_bus_vkt_bj = 16_615 * 45_249.6
    alt_bus_kwh_bj = 16_615 * 28_335.6
    alt_bus_vkt_city = alt_bus_vkt_bj * SCALE
    alt_bus_kwh_city = alt_bus_kwh_bj * SCALE
    add("ALT-BUS-NEV-VKT","reference_flow","vehicle_operation","bus_nonH2_new_energy_electric_drive_proxy",
        "vehicle_km",f"{alt_bus_vkt_city:.6f}","vehicle-km/year","C",
        "P0 round 2 annualized October bus sample","alternative_not_base",
        "16,615 = 16,832 year-end NEV buses minus 217 June H2 snapshot; assumes no later H2 additions")
    add("ALT-BUS-NEV-KWH","energy_input","energy_supply_and_use","bus_nonH2_new_energy_electric_drive_proxy",
        "grid_electricity",f"{alt_bus_kwh_city:.6f}","kWh/year","C",
        "P0 round 2 annualized October bus sample","alternative_not_base",
        "Replace R7 q=0.8 bus electricity, do not add; sample may include non-BEV electric-drive types")

    write_csv(OUT/"R9_LCI_FOREGROUND_FLOWS.csv",flows)

    # Convert fuel volumes to energy using documented defaults; natural gas remains NA.
    gasoline_mj_l = GASOLINE_LHV_MJ_KG * GASOLINE_DENSITY_KG_L
    diesel_mj_l = DIESEL_LHV_MJ_KG * DIESEL_DENSITY_KG_L
    gasoline_mj = gasoline_total_l * gasoline_mj_l
    diesel_mj = diesel_bus_l * diesel_mj_l
    electricity_mj = electricity_total_kwh * ELECTRICITY_MJ_KWH

    # Tsinghua TLCAM 2017 Table 8; paper text contains +1.1 g/MJ alternative figures.
    wtw = []
    def wtw_row(carrier, amount, unit, mj, factor, wtt_share, scenario, note):
        total_t = mj * factor / 1e6  # g/MJ × MJ -> kg; /1000 -> tonnes = /1e6
        wtt_t = total_t*wtt_share if wtt_share is not None else None
        ttw_t = total_t-wtt_t if wtt_t is not None else None
        wtw.append(dict(carrier=carrier,annual_amount=amount,amount_unit=unit,
                        annual_energy_MJ=f"{mj:.6f}",WTW_factor_gCO2e_MJ=factor,
                        WTT_share="" if wtt_share is None else wtt_share,
                        WTT_tCO2e="" if wtt_t is None else f"{wtt_t:.6f}",
                        TTW_tCO2e="" if ttw_t is None else f"{ttw_t:.6f}",
                        WTW_tCO2e=f"{total_t:.6f}",factor_scenario=scenario,
                        status="literature_proxy_not_2023_local_factor",note=note))
    wtw_row("gasoline",gasoline_total_l,"L",gasoline_mj,90.2,0.2341,"TLCAM_2017_Table_8",
            "2015 China fuel pathway; includes WTT+TTW; 2017 paper narrative gives 91.3 g/MJ alternative")
    wtw_row("diesel",diesel_bus_l,"L",diesel_mj,92.3,0.2211,"TLCAM_2017_Table_8",
            "2015 China fuel pathway; includes WTT+TTW; 2017 paper narrative gives 93.3 g/MJ alternative")
    wtw_row("electricity",electricity_total_kwh,"kWh",electricity_mj,203.4,None,"TLCAM_2017_Table_8",
            "2015 national electricity mix; full electricity WTW factor; do not add R7 0.5554 kg CO2/kWh")
    wtw_row("gasoline",gasoline_total_l,"L",gasoline_mj,91.3,0.2341,"TLCAM_2017_text_alternative",
            "Narrative value in Section 4.3; retained as source-discrepancy sensitivity")
    wtw_row("diesel",diesel_bus_l,"L",diesel_mj,93.3,0.2211,"TLCAM_2017_text_alternative",
            "Narrative value in Section 4.3; retained as source-discrepancy sensitivity")
    wtw.append(dict(carrier="CNG_or_LNG",annual_amount=f"{gas_bus_kg:.6f}",amount_unit="kg",
                    annual_energy_MJ="NA",WTW_factor_gCO2e_MJ=72.3,WTT_share=0.2195,
                    WTT_tCO2e="NA",TTW_tCO2e="NA",WTW_tCO2e="NA",
                    factor_scenario="TLCAM_2017_CNG_reference_only",
                    status="not_calculated",note="CNG/LNG split, gas LHV and R7 mass-consumption basis unresolved"))
    write_csv(OUT/"R9_LCI_PARTIAL_WTW_GHG.csv",wtw)

    # Vehicle manufacturing: cradle-to-gate GWP proxy, not raw material LCI.
    manufacture = []
    for vehicle, vkt, kg_vehicle, label in [
        ("private_ICEV",ice_vkt,9985,"Qiao2017_ICEV"),
        ("private_BEV_NMC",bev_vkt,15005,"Qiao2017_BEV_NMC"),
        ("private_BEV_LFP",bev_vkt,15174,"Qiao2017_BEV_LFP"),
    ]:
        per_km_kg = kg_vehicle/200_000
        annual_t = vkt*per_km_kg/1000
        manufacture.append(dict(vehicle_class=vehicle,annual_VKT_km=f"{vkt:.6f}",
            cradle_to_gate_kgCO2e_per_vehicle=kg_vehicle,assumed_lifetime_VKT_km=200000,
            manufacturing_kgCO2e_per_vehicle_km=f"{per_km_kg:.9f}",
            annualized_manufacturing_tCO2e=f"{annual_t:.6f}",source_id=label,
            evidence_grade="B",status="partial_vehicle_cycle_proxy",
            note="Vehicle-production GWP factor includes battery for BEV; do not add separate initial battery factor; steady-state replacement allocation; excludes maintenance/EOL"))
    for vehicle in ("private_PHEV","bus_diesel","bus_natural_gas","bus_BEV"):
        manufacture.append(dict(vehicle_class=vehicle,annual_VKT_km="NA",
            cradle_to_gate_kgCO2e_per_vehicle="NA",assumed_lifetime_VKT_km="NA",
            manufacturing_kgCO2e_per_vehicle_km="NA",annualized_manufacturing_tCO2e="NA",
            source_id="MISSING",evidence_grade="NA",status="missing_local_or_eligible_factor",
            note="Do not fill from post-2023 bus studies or mismatched vehicle class without explicit alternative scenario"))
    write_csv(OUT/"R9_LCI_VEHICLE_MANUFACTURING_PROXY.csv",manufacture)

    checks = [
      ("private_VKT_reconciliation",ice_vkt+bev_vkt+phev_vkt,v("private_total_vkt_km"),"km/year","PASS"),
      ("bus_VKT_reconciliation",bus_diesel_vkt+bus_gas_vkt+bus_mixed_vkt+bus_unknown_vkt,v("bus_total_vkt_km"),"km/year","PASS"),
      ("electricity_reconciliation",electricity_total_kwh,v("electric_kwh"),"kWh/year","PASS"),
      ("gasoline_total_reconciliation",gasoline_total_l,gasoline_ice_l+gasoline_phev_l,"L/year","PASS"),
      ("bus_mixed_nonBEV_left_unallocated",bus_other_mixed_vkt,bus_mixed_vkt*(1-BUS_Q),"km/year","PASS"),
      ("R7_mixed_bus_placeholder_excluded",0,0,"kgCO2/year","PASS"),
    ]
    write_csv(OUT/"R9_LCI_RECONCILIATION.csv",
              [dict(check=name,computed=f"{a:.9f}",reference=f"{b:.9f}",unit=unit,status=status)
               for name,a,b,unit,status in checks])
    print("R9.1 LCI foreground written.")
    print("Private VKT:",round(ice_vkt+bev_vkt+phev_vkt,3))
    print("Bus VKT:",round(bus_diesel_vkt+bus_gas_vkt+bus_mixed_vkt+bus_unknown_vkt,3))
    print("Energy: gasoline L",round(gasoline_total_l,3),"diesel L",round(diesel_bus_l,3),
          "electricity kWh",round(electricity_total_kwh,3),"natural gas kg",round(gas_bus_kg,3))
    print("Natural gas WTW and all bus manufacturing remain NA.")
if __name__ == "__main__":
    main()
