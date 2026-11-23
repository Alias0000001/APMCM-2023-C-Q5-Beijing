# Beijing data audit — initial archive

Audit date: 2026-11-23

## 1. Official population and vehicle statistics

The Beijing 2023 Statistical Communiqué reports:
- Year-end resident population: 21.858 million.
- Private automobiles: 5.431 million.
- Private passenger vehicles within private automobiles: 5.073 million.
- New-energy passenger vehicles within private automobiles: 528,000.

**Audit decision:** keep all four fields separately. The 5.431 million private-automobile count must not replace the 5.073 million private-passenger count. The 528,000 new-energy passenger vehicles must not be split into BEV/PHEV without a cross-tab.

## 2. Public bus and operator statistics

The Beijing city transport summary reports 23,385 public bus operating vehicles and annual passenger volume of about 2.09 billion trips. The Beijing Public Transport Group historical table provides more detailed 2023 values under the source category 公共电汽车:
- 23,385 operating vehicles;
- 1.151 billion vehicle-km;
- 2.08687 billion passenger trips.

The same table separately reports group-wide totals:
- 33,133 operating vehicles;
- 1.47566 billion vehicle-km;
- 2.14368 billion passenger trips.

**Audit decision:** preserve the source category label and keep the category totals separate from group-wide totals. Do not interpret 公共电汽车 as proof that all vehicles are battery-electric BEVs. The table does not provide a BEV/PHEV/ICE propulsion split. Passenger trips are not PKM.

## 3. Electricity factor

The 2023 Beijing provincial average electricity CO2 factor is 0.5554 kg CO2/kWh. The national announcement was published on 2025-12-31.

**Audit decision:** it may be used as a retrospective factor for 2023 operational electricity CO2 accounting, with the publication date visible. It is not a full life-cycle CO2e factor and should not be used as such.

## 4. PHEV utility factor

The seven-city PHEV charging-pattern study reports Beijing actual utility factors of 0.66 for PHEV50 and 0.79 for PHEV80.

**Audit decision:** retain them as range-specific literature evidence. A fleet-wide Beijing PHEV utility factor requires the fleet's electric-range mix and a justification that the study's technology/charging patterns remain applicable to the 2023 fleet.

## 5. Private-car VKT evidence

A prior working source register records Beijing central-urban-area private passenger-car annual mileage of 12,168 km in 2019 and 10,382 km in 2020 from the Beijing Transport Development Annual Report 2021.

**Audit decision:** retain these as historical local cross-checks only. The original PDF and exact page/table are not archived in this repository yet. The 2020 value is affected by pandemic-era travel conditions. Neither value is a 2023 observation or a BEV/PHEV-specific mileage.

The 10,300 km/year value in Ma et al. is a 2019 national private passenger-car fleet mean, not a Beijing ICE-only mean. The 6,210 km/year BEV value comes from a multi-market public research preview and is not a Beijing-specific sample estimate. Both remain quarantined as external comparisons.

## 6. Zenodo record 13852045

The record supports two processed figure-data files for a seven-city Chinese vehicle-use study, with a dataset period of 2020-11-01 to 2021-10-31. These are processed figure-supporting data, not raw GPS or trip records.

The prior audit report records:
- Fig1e: 100 percentile rows, six vehicle categories, no missing cells or duplicate rows, monotone CDFs, published MD5 match.
- FigSI5: 84 raw rows, including 42 fully blank separators; 42 valid rows remain after dropping only fully blank rows on an analysis copy; seven cities and six vehicle categories; published MD5 match.
- Fig1e private-car P50 in the uploaded CSV is 37 km, while the article narrative reports about 30 km. Unresolved.
- FigSI5 metadata lists the unit as “-”; do not label it km/day or annualize it until the figure axis/method is confirmed.
- Fig1e P100 values are close to 500 for all six categories; possible ceiling/truncation requires source-method review.
- Neither file separates BEV from PHEV, provides individual vehicle observations, covers Beijing 2023, or identifies the private-car urban VKT share alpha_P.

The raw CSV bytes are not currently committed to this repository. The audit metadata and audit script are stored separately. Do not recreate the raw CSVs from summary statistics.

## 7. Baseline blockers

The following inputs remain missing or unresolved:
- Beijing 2023 private passenger-car annual VKT, preferably by propulsion type.
- Private passenger BEV/PHEV vehicle-stock cross-tab.
- Public bus propulsion split and matching VKT by propulsion type.
- Bus passenger-kilometres or average passenger trip distance.
- Private-car urban VKT share alpha_P based on distance, not trip count.
- Vehicle-specific fuel and electricity consumption under matching duty cycles.
- Vehicle and battery manufacturing, maintenance, replacement, and end-of-life factors with consistent boundaries.
- LCIA method/version and factor mapping.

## 8. Release decision

The repository contains a usable official-statistics baseline and a reproducible population-scaling calculation. It does **not** yet contain enough evidence for a defensible full S0 life-cycle result. Keep missing values blank and continue targeted collection rather than filling them with unsupported point estimates.
