## R9.7C manufacturing-factor audit — 2026-11-24

**Read [R9.7C audit](08_Reports/R9_7C_MANUFACTURING_FACTOR_AUDIT.md).** The contest-time branch now contains:
- bus manufacturing factors from Lin et al. (2015), derived from raw-material + assembly GWP per PKM and the paper's effective occupancy/lifetime;
- an independent Hangzhou (2018) bus manufacturing CO2 boundary alternative, retained separately due battery-pack accounting ambiguity;
- PHEV production factors from Xiong et al. (2019), with Yang et al. (2021) matched CO2 production ranges as a parallel check;
- Qiao2017 + Xiong2019 private-car production GWP proxy, integrated with Lin2015 bus GWP and R9.7B WTW for a clearly labelled partial-LCA scenario matrix;
- [component-level derivations](02_Cleaned_Data/R9_7C_MANUFACTURING_DERIVATION.csv), [factor register](02_Cleaned_Data/R9_7C_MANUFACTURING_FACTOR_REGISTER.csv), [bus alternatives](02_Cleaned_Data/R9_7C_BUS_FACTOR_BOUNDARY_ALTERNATIVES.csv), and [partial LCA GWP results](02_Cleaned_Data/R9_7C_PARTIAL_LCA_GWP_SCENARIOS.csv).

Partial S0→S3 GWP reduction is 14.23%; S0→S4 is 39.94%. This is not a complete cradle-to-grave total: maintenance, EOL, infrastructure and non-exhaust emissions remain outside the boundary. The workflow runs R9.7A/B/C and 16 regression tests; see [latest Actions run](https://github.com/Alias0000001/APMCM-2023-C-Q5-Beijing/actions/runs/45366032299). All work remains on `work/r96-figures-energy-audit-20261124`, not main.

## R9.6 branch update — 2026-11-24

Work is not required for the current evidence and figure workflow. See branch work/r96-figures-energy-audit-20261124 and the R9.6 data/figure audit at 08_Reports/R9_6_DATA_AND_FIGURE_AUDIT.md. It:
- corrects private-BEV use intensity from 0.152 to 0.160 kWh/km after Table 4-1 row verification;
- records the charging meter boundary as unresolved and keeps charging-loss sensitivity separate;
- adds historical Beijing bus manufacturing GWP proxies from Lin et al. (2015);
- keeps 2023 bus-only PKM as NA pending AFC OD/route passenger-turnover data;
- adds a CSV-driven SVG generator, regression tests, and a GitHub Actions workflow;
- does not write to main.

See 08_Reports/R9_6_TEST_RUNBOOK.md for GitHub Actions and local Python alternatives.

# APMCM 2023 C Problem 5 — Beijing

## Latest: R9.5 sensitivity and paper draft (2026-11-24)

**Read [R9.5 sensitivity report](08_Reports/R9_5_SENSITIVITY_REPORT.md)** and [English paper draft](09_Paper_Draft/R9_5_Paper_Draft_EN.md). R9.5 adds:
- [lifetime-mileage sensitivity](07_LCA_LCIA/R9_5_LIFETIME_SENSITIVITY.csv) (15 rows);
- [electricity-factor sensitivity](07_LCA_LCIA/R9_5_GRID_FACTOR_SENSITIVITY.csv) (6 rows);
- [grid × lifetime factorial](07_LCA_LCIA/R9_5_GRID_LIFETIME_FACTORIAL.csv) (18 rows);
- [BEV break-even electricity factors](07_LCA_LCIA/R9_5_BREAK_EVEN_GRID_FACTOR.csv) (10 rows);
- [battery-only factor sensitivity](07_LCA_LCIA/R9_5_BATTERY_FACTOR_SENSITIVITY.csv) (44 rows);
- [retrospective electricity cross-checks](07_LCA_LCIA/R9_5_RETROSPECTIVE_GRID_CROSSCHECK.csv);
- [24 audit checks](07_LCA_LCIA/R9_5_TESTS.csv).

Run `python 06_S0_Calculation/r9_5_sensitivity.py`. Strict contest-time results retain pre-2023 Peng2017 WTW factors; 2023 official MEE electricity factors published in 2025 are retrospective checks only. Battery-only GWP is never added to Qiao BEV production. See [paper style research and figure standards](09_Paper_Draft/论文写作与图表风格研究.md) and [R9.5 vector figures](09_Paper_Draft/figures/).

## Previous: R9.4 gated integration (2026-11-24)

**Read [R9.4 integration report](08_Reports/R9_4_LCI_LCIA_INTEGRATION_REPORT.md).** This version integrates the R7/R9 foreground activity into **three intentionally separate reporting domains**:
- [physical pollutant masses, kg/year](07_LCA_LCIA/R9_4_PHYSICAL_FLOW_LEDGER.csv) — partial Yang2021 life-cycle sub-stages, no full-LCA totals;
- [two-stage GWP100 CO2e screening](07_LCA_LCIA/R9_4_TWO_STAGE_GWP100_SCREENING.csv) — Qiao2017 complete vehicle production + Peng2017 fuel/electricity WTW, for ICEV and BEV alternatives only; PHEV/bus production NA;
- [battery-only ReCiPe LCIA](07_LCA_LCIA/R9_4_BATTERY_RECIPE_ONLY.csv) — Sun2020 NCM622, manufacture and hypothetical 100% hydromet recycling; not added to either prior domain.

**Model script**: `python 06_S0_Calculation/r9_4_integrate_lci.py`. See [coverage matrix](07_LCA_LCIA/R9_4_STAGE_COVERAGE_MATRIX.csv) and [32 independent consistency checks](07_LCA_LCIA/R9_4_INTEGRATION_TESTS.csv). Two upstream CSV issues (168g/MJ electricity factor column alignment, PHEV electricity formula reconciliation) were corrected. No claim of full citywide cradle-to-grave results or GitHub CI pass.

## Previous: R9.3 NCM622 battery and Beijing historical bus LCI (2026-11-24)

**Read [R9.3 report](08_Reports/R9_3_NCM622_BATTERY_AND_BUS_LCI_REPORT.md)** for the detailed NCM622 material BOM, factory and recycling inventories, ReCiPe LCIA factors, and 2015 Beijing bus historical-transfer stress scenario. New models are **separate modules**: the Sun2020 battery pack mass does not match the Yang2021 vehicle battery mass, and the 2015 bus electricity/fuel system is not the 2023 observed fleet.

Run:
- `python 06_S0_Calculation/r9_3_ncm622_battery_lci.py`
- `python 06_S0_Calculation/r9_3_legacy_beijing_bus_lci.py`

See [battery source BOM](07_LCA_LCIA/R9_3_NCM622_PACK_BOM.csv), [annual battery LCIA scenarios](07_LCA_LCIA/R9_3_NCM622_BATTERY_LCIA_SCENARIOS.csv), [historical bus stress table](07_LCA_LCIA/R9_3_BEIJING_2015_BUS_TRANSFER_STRESS.csv), and [no-double-count integration rules](07_LCA_LCIA/R9_3_MODULE_INTEGRATION_RULES.csv). These files are conditional model outputs, not a completed 2023 city-wide LCA.

## Previous: R9.2 lifecycle inventory construction (2026-11-24)

**Read [R9.2 construction report](08_Reports/R9_LCI_CONSTRUCTION_ROUND_02_PASSENGER_CAR.md), [LCI method](07_LCA_LCIA/R9_LCI_METHOD.md), and [stage coverage ledger](07_LCA_LCIA/R9_LCI_STAGE_COVERAGE.csv).** R9 has created a partial foreground LCI for private ICEV/BEV/PHEV, a partial bus diesel/electric use-stage module, and separate battery GWP scenarios. Missing flows remain NA. Do not describe current outputs as a completed full-city LCA.

Reproducible scripts:
- `python 06_S0_Calculation/r9_lci_foreground.py`
- `python 06_S0_Calculation/r9_lci_passenger_car_module.py`
- `python 06_S0_Calculation/r9_lci_bus_use_module.py`

Core limits: bus manufacturing, bus natural-gas WTW, mixed/unknown bus energy, vehicle assembly, battery manufacturing pollutant flows, non-exhaust emissions, and full end-of-life recycling remain incomplete. 2023 activity data published after the competition cutoff are used only for retrospective reconstruction, not claimed as contemporaneously available.

## R5 baseline: public-source corrections (2026-11-24)


**Read [R5 report](08_Reports/R5_PUBLIC_SOURCES_DATA_UPGRADE.md) and [R5 audit](03_Data_Audit/R5_PUBLIC_SOURCE_AUDIT.md) first.** The previous public departmental reporting login URL is not a public download service and should not be recommended to users. R5 uses a public 2023-04-23 bus-operator interview: 1,495 diesel, 6,795 natural gas, 15,451 mixed new-energy electric-drive buses and 6 unclassified from total 23,747. This is a 2023-April snapshot, not 2023 year-end, and the mixed electric-drive group is NOT pure BEV. R5 also replaces the old private BEV annualization of 18,723.84 km with **18,619.2 km/year as a scenario** based on the directly reported 2023-October monthly mileage 1,551.6 km. Annualized monthly values and VKT by propulsion are proxies, not 2023 odometer observations.

New datasets: `02_Cleaned_Data/R5_bus_2023_04_fleet_snapshot.csv`, `R5_bus_vkt_allocation_scenarios.csv`, `R5_private_bev_2023_october_observed.csv`, `R5_private_VKT_corrected_sensitivity.csv`. Re-run `python 06_S0_Calculation/r5_public_proxy_scenarios.py`.

Earlier R2–R4 model files remain available as archive/contrast and must not override R5 corrections.



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
3. Beijing's 2020-revised quota rules define quota-policy new-energy small passenger cars as pure-electric; PHEVs may use ordinary indicators. The 52.8w statistical private-NEV count still lacks a local propulsion cross-tab. The national 76.04% BEV share is now only a comparator, not a Beijing central estimate. Use `02_Cleaned_Data/P0_private_VKT_policy_mix_sensitivity.csv` for the 0/5/10/23.96% PHEV-share and 250/300/365 active-day grid.
4. Bus structure: 16,832 new-energy buses; 217 hydrogen buses in a 2023-06-19 official snapshot; non-hydrogen new-energy bus proxy 16,615, assuming no H2 additions after the snapshot. Clean-energy plus new-energy share is 94.7%. The inferred clean-energy and other fleet counts are approximate; CNG/LNG and diesel/hybrid/trolley splits remain unknown.
5. Electric-bus October 2023 monthly VKT 3,770.8 km and electricity 2,361.3 kWh; annualized per-vehicle VKT 45,249.6 km. Estimated BEV/electric-drive VKT is 751.8 million km/year, about 65.3% of the 1.151 billion km mixed public-bus total; the remaining 399.2 million km is left unallocated.

The P0 estimates are documented in `08_Reports/P0_DATA_COLLECTION_ROUND_02.md`, `08_Reports/P0_DATA_COLLECTION_ROUND_03_ALTERNATIVE_ACCESS.md`, and `08_Reports/P0_DATA_COLLECTION_ROUND_04_PRIVATE_NEV_POLICY_AUDIT.md`, with the consolidated audit in `03_Data_Audit/P0_EVIDENCE_AUDIT.md`. Reproducible scripts: `06_S0_Calculation/p0_vkt_propulsion_scenarios.py` (legacy national-mix comparator only), `06_S0_Calculation/p0_round03_alternative_sources.py`, and `06_S0_Calculation/p0_private_vkt_policy_mix_sensitivity.py` (policy-aware sensitivity grid).

## Round 3 additions — 2026-11-23

1. Replaced the inaccessible departmental reporting IP with the Beijing Municipal Transport Commission information-disclosure route and the Beijing Public Data Open Platform's data-request function. The old `43.254.24.235:9999` URL is a departmental reporting backend, not a public download portal.
2. Added a 2020–2025 Beijing Bus Group activity series. The source category `公共电汽车` is not a BEV-only category. 2023: 23,385 operating vehicles, 1.151 billion vehicle-km, 2.08687 billion passenger trips.
3. Added pre-cutoff 2023H1 bus activity from the September 2023 MTN prospectus: 552 million vehicle-km and 977 million passenger trips. Added fuel/electric-traction accounting cost cross-checks; these are not physical energy quantities.
4. Added a 2021 Beijing PHEV subsample: 45 vehicles, 10,372 effective vehicle-days, 488,521 km, 47.1 km/effective vehicle-day. Annual active-day conversions are sensitivity scenarios only.
5. Added a 15,137 new-energy bus count from a 2023-11-06 exchange disclosure, but its exact snapshot date is unspecified; cross-check only.
6. Audited the open-data portal's bus-stop dataset (route/stop sequence, no listed coordinates) and its AI-generated 1,000-row synthetic bus-trajectory dataset (not real observations; do not use for VKT).

New derived files: `02_Cleaned_Data/P0_bus_activity_timeseries_2020_2025.csv`, `P0_bus_operating_cost_crosscheck_2022_2023H1.csv`, `P0_BJ_PHEV_daily_VKT_sensitivity.csv`, `P0_bus_fleet_count_evidence.csv`, and `P0_private_VKT_policy_mix_sensitivity.csv`.

## Round 4 correction — private BEV/PHEV stock split

- Beijing's 2020-revised quota rules (in force in 2023) define quota-policy new-energy small passenger cars as pure-electric. The 2023 quota was 70,000 new-energy indicators and 30,000 ordinary indicators.
- A 2025 official clarification states ordinary indicators can purchase PHEV/range-extender vehicles and that the policy has existed since 2021.
- The 528,000 private new-energy passenger-car stock still lacks a public BEV/PHEV cross-tab. The national 76.04% BEV share is now a comparator only, not a Beijing central estimate.
- New policy-aware grid: `02_Cleaned_Data/P0_private_VKT_policy_mix_sensitivity.csv`; script: `06_S0_Calculation/p0_private_vkt_policy_mix_sensitivity.py`.
- Likely holder of vehicle-registration fuel-type data: Beijing Public Security Traffic Management Bureau. The Beijing Public Security Bureau provides an official information-disclosure route: https://gaj.beijing.gov.cn/zfxxgk/zfxxgkzn/index.html. Online navigation: 警务公开 → 依申请公开网页申请.

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
- Beijing Public Security Bureau information disclosure guide: https://gaj.beijing.gov.cn/zfxxgk/zfxxgkzn/index.html
- Beijing Public Security Bureau application form page: https://gaj.beijing.gov.cn/wsgs/bsbg/qita/202112/t20211231_2580778.html
- Beijing public data open platform: https://data.beijing.gov.cn/
- Beijing local PHEV actual travel study: https://www.mdpi.com/2032-6653/12/4/169
- Beijing Bus Group 2023 MTN prospectus: https://qxb-pdf-osscache.qixin.com/AnBaseinfo/466e28c65cb1a52063e0a528c963497c.pdf
- 2023 provincial electricity CO2 factor announcement: https://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/202512/t20251231_1139517.html
- Zenodo record 13852045: https://zenodo.org/records/13852045
- PHEV utility-factor study: https://www.mdpi.com/2032-6653/12/4/169
- Shanghai private-PHEV GPS study: https://www.mdpi.com/2071-1050/11/20/5761

## Reproducibility

Run `python 06_S0_Calculation/scale_official_inputs.py` for official population-scaled inputs, `python 06_S0_Calculation/p0_vkt_propulsion_scenarios.py` for the first private-car and bus P0 scenarios, and `python 06_S0_Calculation/p0_round03_alternative_sources.py` for the round-3 bus activity/cost and local PHEV sensitivity tables. The latter makes proxy assumptions explicit and does not fabricate a CNG/LNG or non-BEV bus VKT split.
