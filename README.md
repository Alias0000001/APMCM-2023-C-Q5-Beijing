# APMCM 2023 C Problem 5 — Beijing

**Repository purpose:** a traceable data, audit, and calculation workspace for the Beijing-based analysis of Problem 5.

**Status:** initial structure; not a completed or fully validated S0 result.
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

## Known Beijing-related evidence currently in the working record

1. Beijing 2023 Statistical Communiqué: year-end resident population 21.858 million; private automobiles 5.431 million; private passenger vehicles 5.073 million; new-energy private passenger vehicles 528,000. These are different statistical categories and must not be conflated.
2. Beijing Public Transport Group historical statistics for 2023: public electric-bus operating vehicles 23,385; annual operating mileage 1.151 billion vehicle-km; passenger trips 2.08687 billion. Group-wide total operating mileage is reported separately as 1.47566 billion vehicle-km and must not be substituted for public electric-bus mileage.
3. Beijing 2023 electricity CO2 factor: 0.5554 kg CO2/kWh, published 2025-12-31. This is a retrospective factor for the 2023 reference year, not a value published during 2023.
4. Zenodo record 13852045 includes processed daily-distance figure data for seven Chinese cities, including Beijing. It is not raw GPS/trip data. The FigSI5 unit is unspecified in the metadata and must not be annualized until resolved.
5. Beijing PHEV utility-factor evidence distinguishes PHEV50 (0.66) and PHEV80 (0.79); a fleet-wide value requires the fleet's electric-range mix.
6. Shanghai private-PHEV GPS mean annual-window distance 14,774.95 km is an external historical proxy, not a Beijing observation.
7. The 10,300 km ICE and 6,210 km BEV annual-mileage values appearing in earlier working notes are not yet admitted as Beijing-specific parameters; their exact source scope and transferability must be recorded.

The source register and audit notes are authoritative for use restrictions.

## Core model rules

- Keep vehicle-kilometres (VKT) and passenger-kilometres (PKM) distinct.
- Do not infer annual mean VKT by multiplying a median daily distance by 365.
- Distinguish vehicle-stock electrification share from VKT electrification share.
- Keep local road emissions separate from full life-cycle burdens to avoid double counting.
- Distinguish CO2 from CO2e, and grid-average from life-cycle electricity factors.
- Population scaling to one million is a baseline approximation and must be accompanied by a limitation statement and sensitivity test.

## Key references

- Beijing 2023 Statistical Communiqué: https://tjj.beijing.gov.cn/tjsj_31433/tjgb_31445/ndgb_31446/202403/t20240321_3595860.html
- Beijing Public Transport Group statistics: https://www.bjbus.com/home/fun_statistics.php
- 2023 provincial electricity CO2 factor announcement: https://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/202512/t20251231_1139517.html
- Zenodo record 13852045: https://zenodo.org/records/13852045
- PHEV utility-factor study: https://www.mdpi.com/2032-6653/12/4/169
- Shanghai private-PHEV GPS study: https://www.mdpi.com/2071-1050/11/20/5761

## Reproducibility

The calculation script in `06_S0_Calculation/` only scales documented official observations. It intentionally does not invent private-car VKT, private BEV/PHEV counts, bus PKM, or a private-car BEV/PHEV split when the source does not provide them.
