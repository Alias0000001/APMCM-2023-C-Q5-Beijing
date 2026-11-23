# APMCM 2023 C Problem 5 — Beijing

**Repository purpose:** a traceable data, audit, and calculation workspace for the Beijing-based analysis of Problem 5.

**Status:** auditable retrospective 2023 data baseline with P0 VKT and bus-propulsion scenario estimates; most 2023 observation sources were published after 2023-12-31. Exact Beijing private BEV/PHEV cross-tab and propulsion-specific non-BEV bus VKT remain unavailable.
**Reference year:** 2023 wherever a source provides 2023 observations.
**Population target in the problem:** 1,000,000 residents.
**City anchor:** Beijing; each source's exact geographic boundary must still be checked before use.

## Data governance

Every parameter must retain its observation year, publication year, geography, vehicle population, unit, system boundary, source, and verification status. Values are classified as:
- **A — official observation/statistic**
- **B — peer-reviewed or institutional literature evidence**
- **C — derived estimate or transferred proxy**
- **D — assumption / scenario setting**

Never relabel a proxy or derived estimate as a Beijing observation. Preserve raw files unchanged. If the original file is not physically archived, record its absence; do not recreate or fabricate it.

## Repository structure

- `00_Project_Management/` — scope, conventions, and version log
- `01_Raw_Data/` — source-file inventory and original files when available
- `02_Cleaned_Data/` — documented analysis copies
- `03_Data_Audit/` — quality checks, hash records, and discrepancy log
- `04_References/` — source register
- `05_Model_Inputs/` — parameter register and eligibility flags
- `06_S0_Calculation/` — reproducible scaling and checks
- `07_LCA_LCIA/` — life-cycle inventory and impact-assessment inputs
- `08_Reports/` — round reports and decisions
- `99_Archive/` — superseded versions

## P0 findings added on 2026-11-23

1. Private passenger fleet: 5.073 million vehicles, including 528,000 NEVs; non-NEV remainder 4.545 million.
2. Private-car daily activity anchor: 28.4 vehicle-km/day, annualized to 10,366 km/vehicle-year. Private BEV October 2023 charging statistics imply 9.2 sessions/month × 169.6 km/session = 1,560.32 km/month, annualized to 18,723.84 km/year. PHEV uses Shanghai 2018 GPS mean 14,774.95 km/year as an external proxy.
3. Central private NEV split scenario uses national 2023 BEV stock share 76.04% (not a Beijing measurement), giving about 401,491 BEVs and 126,509 PHEVs. Low/high PHEV shares are 10% and 30%.
4. Bus structure: 16,832 new-energy buses; 217 hydrogen buses in a 2023-06-19 official snapshot; non-hydrogen new-energy bus proxy 16,615, assuming no H2 additions after the snapshot. Clean-energy plus new-energy share is 94.7%. The inferred clean-energy and other fleet counts are approximate; CNG/LNG and diesel/hybrid/trolley splits remain unknown.
5. Electric-bus October 2023 monthly VKT 3,770.8 km and electricity 2,361.3 kWh; annualized per-vehicle VKT 45,249.6 km. Estimated BEV/electric-drive VKT is 751.8 million km/year, about 65.3% of the 1.151 billion km mixed public-bus total; the remaining 399.2 million km is left unallocated.

The P0 estimates are documented in `08_Reports/P0_DATA_COLLECTION_ROUND_02.md` and `08_Reports/P0_DATA_COLLECTION_ROUND_03_ALTERNATIVE_ACCESS.md`, with the consolidated audit in `03_Data_Audit/P0_EVIDENCE_AUDIT.md`. Reproducible scripts: `06_S0_Calculation/p0_vkt_propulsion_scenarios.py` and `06_S0_Calculation/p0_round03_alternative_sources.py`.

## Round 3 additions — 2026-11-23

1. Replaced the inaccessible departmental reporting IP with the Beijing Municipal Transport Commission information-disclosure route and the Beijing Public Data Open Platform's data-request function. The old `43.254.24.235:9999` URL is a departmental reporting backend, not a public download portal.
2. Added a 2020–2025 Beijing Bus Group activity series. The source category `公共电汽车` is not a BEV-only category. 2023: 23,385 operating vehicles, 1.151 billion vehicle-km, 2.08687 billion passenger trips.
3. Added pre-cutoff 2023H1 bus activity from the September 2023 MTN prospectus: 552 million vehicle-km and 977 million passenger trips. Added fuel/electric-traction accounting cost cross-checks; these are not physical energy quantities.
4. Added a 2021 Beijing PHEV subsample: 45 vehicles, 10,372 effective vehicle-days, 488,521 km, 47.1 km/effective vehicle-day. Annual active-day conversions are sensitivity scenarios only.
5. Added a 15,137 new-energy bus count from a 2023-11-06 exchange disclosure, but its exact snapshot date is unspecified; cross-check only.
6. Audited the open-data portal's bus-stop dataset (route/stop sequence, no listed coordinates) and its AI-generated 1,000-row synthetic bus-trajectory dataset (not real observations; do not use for VKT).

New derived files: `02_Cleaned_Data/P0_bus_activity_timeseries_2020_2025.csv`, `P0_bus_operating_cost_crosscheck_2022_2023H1.csv`, and `P0_BJ_PHEV_daily_VKT_sensitivity.csv`.

## Known Beijing-related evidence currently in the working record

1. Beijing 2023 Statistical Communiqué: year-end resident population 21.858 million; private automobiles 5.431 million; private passenger vehicles 5.073 million; new-energy private passenger vehicles 528,000. These are different statistical categories and must not be conflated.
2. Beijing Public Transport Group's 2023 historical-statistics table reports the category `公共电汽车`: 23,385 operating vehicles, 1.151 billion vehicle-km, and 2.08687 billion passenger trips. The source also reports group-wide totals of 33,133 vehicles, 1.47566 billion vehicle-km, and 2.14368 billion trips. **Do not interpret the category label as proof that all vehicles are battery-electric BEVs.** The operating-mix and propulsion split require separate evidence.
3. Beijing's 2023 provincial electricity average CO2 factor is 0.5554 kg CO2/kWh, published on 2025-12-31. This is a retrospective factor for the 2023 reference year, not a value published during 2023. It is a CO2 factor, not automatically a full life-cycle CO2e factor.
4. Zenodo record 13852045 includes processed daily-distance figure data for seven Chinese cities, including Beijing. It is not raw GPS/trip data. The FigSI5 unit is unspecified in the metadata and must not be annualized until resolved.
5. Beijing PHEV utility-factor evidence distinguishes PHEV50 (actual UF 0.66) and PHEV80 (actual UF 0.79); a fleet-wide value requires the fleet's electric-range mix.
6. Shanghai private-PHEV GPS mean annual-window distance 14,774.95 km is an external historical proxy, not a Beijing observation.
7. The 10,300 km national ICE and 6,210 km multi-market BEV annual-mileage values from earlier notes remain quarantined; the new Beijing P0 estimates supersede them for the first-pass scenarios, with explicit limitations.

The source register and audit notes are authoritative for use restrictions.

## Core model rules

- Keep vehicle-kilometres (VKT) and passenger-kilometres (PKM) distinct.
- Do not infer annual mean VKT by multiplying a median daily distance by 365.
- Distinguish vehicle-stock electrification share from VKT electrification share.
- Keep local road emissions separate from full life-cycle burdens to avoid double counting.
- Distinguish CO2 from CO2e, and grid-average from life-cycle electricity factors.
- Population scaling to one million is a baseline approximation and must be accompanied by a limitation statement and sensitivity test.
- Do not treat public-transport operating fleet labels as BEV/PHEV classifications without a propulsion cross-tab.

## Key references

- Beijing 2023 Statistical Communiqué: https://tjj.beijing.gov.cn/tjsj_31433/tjgb_31445/ndgb_31446/202403/t20240321_3595860.html
- Beijing Public Transport Group historical statistics: https://www.bjbus.com/home/fun_statistics.php
- Beijing Transport Commission information disclosure guide: https://jtw.beijing.gov.cn/xxgk/zfxxgk/
- Beijing public data open platform: https://data.beijing.gov.cn/
- Beijing local PHEV actual travel study: https://www.mdpi.com/2032-6653/12/4/169
- Beijing Bus Group 2023 MTN prospectus: https://qxb-pdf-osscache.qixin.com/AnBaseinfo/466e28c65cb1a52063e0a528c963497c.pdf
- 2023 provincial electricity CO2 factor announcement: https://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/202512/t20251231_1139517.html
- Zenodo record 13852045: https://zenodo.org/records/13852045
- PHEV utility-factor study: https://www.mdpi.com/2032-6653/12/4/169
- Shanghai private-PHEV GPS study: https://www.mdpi.com/2071-1050/11/20/5761

## Reproducibility

Run `python 06_S0_Calculation/scale_official_inputs.py` for official population-scaled inputs, `python 06_S0_Calculation/p0_vkt_propulsion_scenarios.py` for the first private-car and bus P0 scenarios, and `python 06_S0_Calculation/p0_round03_alternative_sources.py` for the round-3 bus activity/cost and local PHEV sensitivity tables. The latter makes proxy assumptions explicit and does not fabricate a CNG/LNG or non-BEV bus VKT split.
