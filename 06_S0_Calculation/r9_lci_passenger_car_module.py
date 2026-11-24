#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R9.2 passenger-car detailed LCI module based on Yang et al. (2021).

Inputs: R7 S0 annual VKT for ICEV/BEV/PHEV.
Outputs: raw material flows, material-production energy inputs, parts energy,
maintenance/EOL flows, use-stage emissions, and battery-GWP scenarios.
The module is partial: vehicle distribution/assembly and battery pollutant flows
are not complete; it does not create a full-city LCA total.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "02_Cleaned_Data"
OUT = ROOT / "07_LCA_LCIA"
R7_FILE = DATA / "R7_S0_CO2_scenarios.csv"

LIFETIME_VKT = 150_000
PHEV_UF = 0.66
ICE_L100 = 7.5
PHEV_L100 = 7.5
PHEV_KWH100 = 16.0
BEV_KWH_KM = 0.160  # R5_CHARGE private passenger-car row; 15.2 is taxi, not private BEV
GASOLINE_LHV_MJ_KG = 43.07
GASOLINE_DENSITY_KG_L = 0.74
ELECTRICITY_MJ_KWH = 3.6
EOL_DISPOSAL_MJ_KG = 0.370  # 370 kJ/kg from Yang et al. (2021)
DISTRIBUTION_DISTANCE_KM = {"ICEV":1177.94,"BEV":1065.34,"PHEV":1177.94}
DISTRIBUTION_ALPHA_KJ_KG_KM = 0.6  # Wang et al. (2013), adopted by Yang et al. (2021)

VEHICLE_MATERIALS = {
 "steel":{"ICEV":793,"BEV":827,"PHEV":847},
 "cast_iron":{"ICEV":139,"BEV":25,"PHEV":78},
 "cast_aluminum":{"ICEV":28,"BEV":12,"PHEV":66},
 "wrought_aluminum":{"ICEV":59,"BEV":68,"PHEV":23},
 "copper":{"ICEV":24,"BEV":59,"PHEV":56},
 "glass":{"ICEV":37,"BEV":44,"PHEV":38},
 "average_plastic":{"ICEV":141,"BEV":151,"PHEV":138},
 "rubber":{"ICEV":29,"BEV":22,"PHEV":26},
 "other":{"ICEV":23,"BEV":37,"PHEV":27},
 "lead_acid_battery":{"ICEV":15,"BEV":15,"PHEV":15},
 "fluid":{"ICEV":26,"BEV":26,"PHEV":26},
 "tire":{"ICEV":36,"BEV":36,"PHEV":36},
 "lithium_ion_battery":{"ICEV":0,"BEV":286,"PHEV":128},
}
VEHICLE_MASS = {"ICEV":1350,"BEV":1608,"PHEV":1504}
BATTERY_CAPACITY_KWH = {"BEV":40.0,"PHEV":12.8}

# Table 4, Yang et al. (2021). CO2 is kg/kg; all other columns are g/kg.
MATERIAL_EF = {
 "steel":(2.00,3.12,1.90,.74,8.39),
 "cast_iron":(.55,2.52,1.31,.57,3.67),
 "cast_aluminum":(2.62,.47,2.45,.74,7.47),
 "wrought_aluminum":(5.92,1.13,4.92,1.99,24.10),
 "copper":(2.35,.32,5.43,.23,.14),
 "glass":(1.62,.24,2.28,.09919,1.36),
 "average_plastic":(3.05,1.12,5.10,.32,17.46),
 "rubber":(3.62,6.27,5.03,.44,13.75),
 "other":(2.70,1.77,3.42,.66,9.39),
}
POLLUTANTS = ("CO2","VOC","NOx","PM2.5","SO2")

# Table 5: material production energy, MJ/t; batteries, tyres and fluids excluded.
MATERIAL_ENERGY = {
 "steel":{"coal":21300,"electricity":2001,"natural_gas":8277,"coke":12117,"crude_oil":253,"gasoline":3,"diesel":39,"BFG":1087,"COG":494},
 "cast_iron":{"coal":0,"electricity":692,"natural_gas":5742,"coke":2639,"crude_oil":194,"gasoline":2,"diesel":30,"BFG":0,"COG":0},
 "cast_aluminum":{"coal":50426,"electricity":15368,"natural_gas":7977,"coke":0,"crude_oil":0,"gasoline":0,"diesel":0,"BFG":0,"COG":0},
 "wrought_aluminum":{"coal":47802,"electricity":14660,"natural_gas":5699,"coke":0,"crude_oil":0,"gasoline":0,"diesel":0,"BFG":0,"COG":0},
 "copper":{"coal":4387,"electricity":5460,"natural_gas":0,"coke":0,"crude_oil":6812,"gasoline":0,"diesel":9566,"BFG":0,"COG":0},
 "glass":{"coal":3172,"electricity":978,"natural_gas":16125,"coke":0,"crude_oil":326,"gasoline":0,"diesel":0,"BFG":0,"COG":0},
 "average_plastic":{"coal":433,"electricity":1492,"natural_gas":19784,"coke":0,"crude_oil":3566,"gasoline":62,"diesel":197,"BFG":0,"COG":0},
 "rubber":{"coal":0,"electricity":751,"natural_gas":21639,"coke":0,"crude_oil":17661,"gasoline":0,"diesel":0,"BFG":0,"COG":0},
 "other":{"coal":15940,"electricity":5175,"natural_gas":10655,"coke":1845,"crude_oil":3602,"gasoline":8,"diesel":1229,"BFG":136,"COG":62},
}
# Table 7: parts manufacturing energy, MJ/vehicle.
PARTS_ENERGY = {
 "ICEV":{"natural_gas":5816,"coal":3788,"electricity":4180},
 "BEV":{"natural_gas":5688,"coal":3705,"electricity":4089},
 "PHEV":{"natural_gas":5935,"coal":3865,"electricity":4266},
}
# Table 6: life-cycle energy emission factors, kg pollutant/MJ.
ENERGY_EF = {
 "coal":{"CO2":.097500,"VOC":.000247,"NOx":.000046,"PM2.5":.000001,"SO2":.000018},
 "electricity":{"CO2":.190798,"VOC":.000017,"NOx":.000104,"PM2.5":.000014,"SO2":.000113},
 "natural_gas":{"CO2":.064800,"VOC":.000256,"NOx":.000031,"PM2.5":.000001,"SO2":.000018},
 "gasoline":{"CO2":.087700,"VOC":.000123,"NOx":.000028,"PM2.5":.000001,"SO2":.000035},
 "diesel":{"CO2":.090700,"VOC":.000120,"NOx":.000024,"PM2.5":.000001,"SO2":.000026},
}
# Table 10, kg pollutant per vehicle over 150,000 km, including the stated replacements.
MAINTENANCE = {
 "powertrain_coolant":{"replacements":4,"CO2":20.478,"VOC":.088,"NOx":.020,"PM2.5":.002,"SO2":.045},
 "transmission_fluid":{"replacements":2,"CO2":7.145,"VOC":.005,"NOx":.007,"PM2.5":.001,"SO2":.020},
 "brake_fluid":{"replacements":7,"CO2":7.145,"VOC":.005,"NOx":.007,"PM2.5":.001,"SO2":.020},
 "windshield_fluid":{"replacements":11,"CO2":3.345,"VOC":.012,"NOx":.002,"PM2.5":0,"SO2":.002},
 "lead_acid_battery":{"replacements":3,"CO2":182.840,"VOC":.292,"NOx":.075,"PM2.5":.058,"SO2":.204},
 "tire":{"replacements":1,"CO2":206.812,"VOC":.386,"NOx":.202,"PM2.5":.021,"SO2":.471},
}
# ICCT 2021 China battery manufacturing GWP, kgCO2e/kWh.
BATTERY_GWP = {
 "China_weighted_NMC_avg":68.0,"NMC811":68.0,"NMC622":69.0,"NMC111":77.0,"LFP_low":51.0,"LFP_high":56.0,
 "Hao2017_NMC":2912/28,"Hao2017_LFP":3061/28,
 "Lai2022_ternary_low":114.3,"Lai2022_ternary_high":137.0,"Lai2022_LFP":82.5,
}

def read_r7():
    with R7_FILE.open(encoding="utf-8-sig", newline="") as f:
        rows=list(csv.DictReader(f))
    return next(x for x in rows if x["scenario"]=="S0_screening")

def write_csv(path, rows):
    if not rows: return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    r=read_r7()
    num=lambda k:float(r[k])
    vkt={"ICEV":num("ice_vkt_km"),"BEV":num("private_bev_vkt_km"),"PHEV":num("phev_vkt_km")}
    equiv={k:v/LIFETIME_VKT for k,v in vkt.items()}
    # Annual material/reference flows.
    material_rows=[]
    for material, masses in VEHICLE_MATERIALS.items():
        for vehicle in ("ICEV","BEV","PHEV"):
            mass=masses[vehicle]
            factor=MATERIAL_EF.get(material)
            material_rows.append(dict(material=material,vehicle=vehicle,
                kg_per_vehicle=mass,annual_vehicle_equivalent=equiv[vehicle],
                annual_material_kg=mass*equiv[vehicle],
                CO2_factor_kg_per_kg="" if factor is None else factor[0],
                VOC_factor_g_per_kg="" if factor is None else factor[1],
                NOx_factor_g_per_kg="" if factor is None else factor[2],
                PM25_factor_g_per_kg="" if factor is None else factor[3],
                SO2_factor_g_per_kg="" if factor is None else factor[4],
                status="partial_material_flow; factor_NA_for_battery_tire_fluid_lead_acid" if factor is None else "material_factor_from_Yang2021_Table4",
                source_id="Yang2021_Tables3_4"))
    write_csv(OUT/"R9_LCI_PASSENGER_MATERIAL_FLOWS.csv",material_rows)

    # Material production energy inputs, annualized. No emissions are calculated from these
    # because Table 4 already supplies material-production emission factors; adding Table 6
    # to Table 5 here would risk double counting.
    mat_energy_rows=[]
    for vehicle in ("ICEV","BEV","PHEV"):
        per_vehicle={}
        for material, carriers in MATERIAL_ENERGY.items():
            mass=VEHICLE_MATERIALS[material][vehicle]
            for carrier,mj_per_t in carriers.items():
                per_vehicle[carrier]=per_vehicle.get(carrier,0)+mj_per_t*mass/1000
        for carrier,mj in per_vehicle.items():
            mat_energy_rows.append(dict(vehicle=vehicle,energy_carrier=carrier,
                MJ_per_vehicle=mj,annual_vehicle_equivalent=equiv[vehicle],
                annual_energy_MJ=mj*equiv[vehicle],
                source_id="Yang2021_Table5",status="material_production_energy_input",
                note="Table 5 excludes battery, tyres and fluids; not multiplied by energy EF to avoid double counting Table 4 material emissions"))
    write_csv(OUT/"R9_LCI_PASSENGER_MATERIAL_ENERGY.csv",mat_energy_rows)

    # Parts manufacturing energy and associated emissions.
    parts_rows=[]
    for vehicle in ("ICEV","BEV","PHEV"):
        for carrier,mj in PARTS_ENERGY[vehicle].items():
            row=dict(vehicle=vehicle,energy_carrier=carrier,MJ_per_vehicle=mj,
                     annual_vehicle_equivalent=equiv[vehicle],annual_energy_MJ=mj*equiv[vehicle],
                     source_id="Yang2021_Table7",status="parts_manufacturing_energy_input")
            for pollutant,ef in ENERGY_EF[carrier].items():
                row[pollutant+"_kg_per_vehicle"]=mj*ef
                row["annual_"+pollutant+"_kg"]=mj*ef*equiv[vehicle]
            parts_rows.append(row)
    write_csv(OUT/"R9_LCI_PASSENGER_PARTS_ENERGY.csv",parts_rows)

    # Stage emissions from material production, parts manufacturing, distribution,
    # maintenance, EOL and use.
    stage_rows=[]
    for vehicle in ("ICEV","BEV","PHEV"):
        eq=equiv[vehicle]
        # Material production: CO2 in kg, other pollutants converted from g to kg.
        material_per_vehicle={p:0.0 for p in ("CO2","VOC","NOx","PM2.5","SO2")}
        for material,factors in MATERIAL_EF.items():
            mass=VEHICLE_MATERIALS[material][vehicle]
            material_per_vehicle["CO2"]+=mass*factors[0]
            for idx,p in enumerate(("VOC","NOx","PM2.5","SO2"),start=1):
                material_per_vehicle[p]+=mass*factors[idx]/1000
        for p,val in material_per_vehicle.items():
            stage_rows.append(dict(vehicle=vehicle,stage="material_production_major_materials",
                pollutant=p,unit="kg/year",annual_amount=val*eq,
                status="partial_excludes_battery_tire_fluid_lead_acid",
                source_id="Yang2021_Tables3_4"))
        # Parts manufacturing
        for p in POLLUTANTS:
            val=0.0
            for carrier,mj in PARTS_ENERGY[vehicle].items():
                val+=mj*ENERGY_EF[carrier][p]
            stage_rows.append(dict(vehicle=vehicle,stage="parts_manufacturing",
                pollutant=p,unit="kg/year",annual_amount=val*eq,
                status="modelled_from_energy_input_and_life_cycle_EF",
                source_id="Yang2021_Tables6_7"))
        # Vehicle distribution: GDP-weighted delivery distance from Yang2021 Table 8;
        # diesel freight energy factor is an explicit proxy assumption.
        distribution_mj = (DISTRIBUTION_DISTANCE_KM[vehicle] * VEHICLE_MASS[vehicle]
                           * DISTRIBUTION_ALPHA_KJ_KG_KM / 1000)
        for p in POLLUTANTS:
            stage_rows.append(dict(vehicle=vehicle,stage="vehicle_distribution",
                pollutant=p,unit="kg/year",
                annual_amount=distribution_mj*ENERGY_EF["diesel"][p]*eq,
                status="GDP_weighted_distance_and_diesel_EF_proxy",
                source_id="Yang2021_Table8_Wang2013"))
        # Maintenance
        for p in POLLUTANTS:
            val=sum(x[p] for x in MAINTENANCE.values())
            stage_rows.append(dict(vehicle=vehicle,stage="maintenance_replacements",
                pollutant=p,unit="kg/year",annual_amount=val*eq,
                status="150000km_lifetime_replacement_schedule_proxy",
                source_id="Yang2021_Table10"))
        # End of life
        eol_mj=EOL_DISPOSAL_MJ_KG*VEHICLE_MASS[vehicle]
        for p in POLLUTANTS:
            stage_rows.append(dict(vehicle=vehicle,stage="end_of_life_dismantling_energy",
                pollutant=p,unit="kg/year",annual_amount=eol_mj*ENERGY_EF["electricity"][p]*eq,
                status="disposal_energy_only_no_recycling_credit",
                source_id="Yang2021_Eq5_Table6"))
        # Use phase: WTW factors; do not add R7 TTW CO2 again.
        if vehicle=="ICEV":
            fuel_mj={"gasoline":vkt[vehicle]*ICE_L100/100*GASOLINE_LHV_MJ_KG*GASOLINE_DENSITY_KG_L}
        elif vehicle=="BEV":
            fuel_mj={"electricity":vkt[vehicle]*BEV_KWH_KM*ELECTRICITY_MJ_KWH}
        else:
            fuel_mj={
                "gasoline":vkt[vehicle]*(1-PHEV_UF)*PHEV_L100/100*GASOLINE_LHV_MJ_KG*GASOLINE_DENSITY_KG_L,
                "electricity":vkt[vehicle]*PHEV_UF*PHEV_KWH100/100*ELECTRICITY_MJ_KWH,
            }
        for p in POLLUTANTS:
            val=sum(mj*ENERGY_EF[carrier][p] for carrier,mj in fuel_mj.items())
            stage_rows.append(dict(vehicle=vehicle,stage="energy_supply_and_vehicle_use_WTW",
                pollutant=p,unit="kg/year",annual_amount=val,
                status="2018_China_literature_factor_applied_to_R7_activity",
                source_id="Yang2021_Table6"))
    write_csv(OUT/"R9_LCI_PASSENGER_STAGE_EMISSIONS.csv",stage_rows)

    # Distribution activity/energy inputs, kept as a separate foreground module.
    distribution_rows=[]
    for vehicle in ("ICEV","BEV","PHEV"):
        energy_mj=(DISTRIBUTION_DISTANCE_KM[vehicle]*VEHICLE_MASS[vehicle]
                   *DISTRIBUTION_ALPHA_KJ_KG_KM/1000)
        distribution_rows.append(dict(vehicle=vehicle,
            delivery_distance_km=DISTRIBUTION_DISTANCE_KM[vehicle],
            vehicle_mass_kg=VEHICLE_MASS[vehicle],
            energy_intensity_kJ_per_kg_km=DISTRIBUTION_ALPHA_KJ_KG_KM,
            distribution_energy_MJ_per_vehicle=energy_mj,
            assumed_distribution_fuel="diesel",
            annual_vehicle_equivalent=equiv[vehicle],
            annual_distribution_energy_MJ=energy_mj*equiv[vehicle],
            source_id="Yang2021_Table8_Wang2013",
            status="distribution_proxy_not_local_logistics_measurement"))
    write_csv(OUT/"R9_LCI_PASSENGER_DISTRIBUTION.csv",distribution_rows)

    # Battery GWP scenarios, separate from CO2-only stage rows.
    battery_rows=[]
    for vehicle in ("BEV","PHEV"):
        cap=BATTERY_CAPACITY_KWH[vehicle]
        for chemistry,factor in BATTERY_GWP.items():
            battery_rows.append(dict(vehicle=vehicle,battery_chemistry_scenario=chemistry,
                battery_capacity_kWh_per_vehicle=cap,kgCO2e_per_kWh=factor,
                kgCO2e_per_vehicle=cap*factor,annual_vehicle_equivalent=equiv[vehicle],
                annual_battery_GWP_tCO2e=cap*factor*equiv[vehicle]/1000,
                source_id=("ICCT2021" if chemistry.startswith("NMC") or chemistry.startswith("LFP") else
                           "Hao2017" if chemistry.startswith("Hao") else "Lai2022"),
                status="battery_GWP_scenario_not_added_to_CO2_stage_totals",
                note="Yang2021 reference capacities 40kWh BEV and 12.8kWh PHEV; no battery replacement in 150,000km base"))
    write_csv(OUT/"R9_LCI_PASSENGER_BATTERY_GWP.csv",battery_rows)

    # Use-stage physical energy inputs.
    use_rows=[]
    for vehicle in ("ICEV","BEV","PHEV"):
        if vehicle=="ICEV":
            gasoline_l=vkt[vehicle]*ICE_L100/100
            electricity_kwh=0
        elif vehicle=="BEV":
            gasoline_l=0
            electricity_kwh=vkt[vehicle]*BEV_KWH_KM
        else:
            gasoline_l=vkt[vehicle]*(1-PHEV_UF)*PHEV_L100/100
            electricity_kwh=vkt[vehicle]*PHEV_UF*PHEV_KWH100/100
        use_rows.append(dict(vehicle=vehicle,annual_VKT_km=vkt[vehicle],
            gasoline_L=gasoline_l,electricity_kWh=electricity_kwh,
            annual_vehicle_equivalent=equiv[vehicle],
            lifetime_VKT_km_assumed=LIFETIME_VKT,
            source_id="R7_activity_plus_Yang2021_energy_EF",
            status="conditional_foreground_flow"))
    write_csv(OUT/"R9_LCI_PASSENGER_USE_ENERGY.csv",use_rows)

    checks=[
      ("private_VKT_sum",sum(vkt.values()),num("private_total_vkt_km"),"km/year"),
      ("annual_vehicle_equivalent_ICEV",equiv["ICEV"],vkt["ICEV"]/LIFETIME_VKT,"vehicles/year"),
      ("material_mass_ICEV",sum(VEHICLE_MATERIALS[m]["ICEV"] for m in VEHICLE_MATERIALS),1350,"kg/vehicle"),
      ("material_mass_BEV",sum(VEHICLE_MATERIALS[m]["BEV"] for m in VEHICLE_MATERIALS),1608,"kg/vehicle"),
      ("material_mass_PHEV",sum(VEHICLE_MATERIALS[m]["PHEV"] for m in VEHICLE_MATERIALS),1504,"kg/vehicle"),
    ]
    write_csv(OUT/"R9_LCI_PASSENGER_RECONCILIATION.csv",
        [dict(check=name,computed=a,reference=b,unit=unit,status="PASS" if abs(a-b)<1e-4 else "CHECK")
         for name,a,b,unit in checks])
    print("R9.2 passenger-car LCI module written.")
    print("Annual vehicle equivalents:",{k:round(v,3) for k,v in equiv.items()})
    print("Battery production GWP remains separate from CO2-only stage totals.")
    print("Assembly/distribution and battery pollutant flows remain incomplete.")
if __name__=="__main__":
    main()
