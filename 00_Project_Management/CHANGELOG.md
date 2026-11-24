# Change log

## 2026-11-23 — Initial workspace

- Created the Beijing-only repository README.
- Confirmed repository visibility is Public and default branch is main.
- Added the project scope and evidence classification rules.
- Added official Beijing 2023 population/vehicle observations and a source register.
- Added a reproducible linear population-scaling script and initial derived table.
- Added explicit audit notes for the public-bus category, electricity-factor publication date, and unresolved vehicle-technology splits.
- Archived the Zenodo quality-audit metadata available in the working record; the original CSV bytes are not included in this commit.
- No Beijing private BEV/PHEV cross-tab, private-car 2023 VKT, bus PKM, or bus propulsion split has been fabricated.

## 2026-11-23 — P0 data collection round 2

- Added Beijing 2023 private-car daily travel intensity and private BEV charging-session mileage indicators from the 2024 major-city charging infrastructure report.
- Added a PHEV annual-mileage cross-city proxy from the Shanghai 2018 GPS sample.
- Added the Beijing Bus Group 2023 new-energy bus count and clean-energy + new-energy share.
- Added the official 2023 hydrogen-bus snapshot (217 vehicles) and the blank official BMZ04-073-108 reporting-form field list.
- Added central/low/high private BEV-PHEV stock scenarios and a reproducible VKT allocation script.
- Added a provisional bus structure and BEV VKT estimate; the mixed-fleet non-BEV VKT residual remains unallocated.
- Added source, raw-data manifest, parameter, audit, and round-report updates. Original PDF binaries are still external-only and explicitly marked as not archived.

- Added an estimated 470.8 GWh/year of BEV/electric-drive bus electricity use from the 2023-10 monthly sample annualized to 12 months; meter boundary remains to be checked.


## 2026-11-23 — P0 data collection round 3

- Corrected the inaccessible 43.254.24.235 URL classification: it is a departmental reporting backend, not a public download portal.
- Added the Beijing Municipal Transport Commission government information-disclosure route and the Beijing Public Data Open Platform's missing-data request route.
- Added 2020–2025 Beijing Bus Group activity time series and 2023H1 pre-cutoff bus VKT/passenger-trip data from the MTN prospectus.
- Added 2022/2023H1 fuel and electric-traction accounting cost cross-checks, explicitly not treated as physical energy consumption.
- Added a local Beijing PHEV sample (45 vehicles, 10,372 effective vehicle-days, 47.1 km/effective day) and active-day annualization sensitivities.
- Added the pre-cutoff 15,137 new-energy bus count with unknown snapshot date as cross-check only.
- Audited bus-stop open data and an AI-generated synthetic trajectory dataset; the latter is excluded from observed VKT/energy analysis.
- Added reproducible round-3 script, four cleaned datasets, parameter/source/raw manifests, audit and Chinese round report.


## 2026-11-23 — Private BEV/PHEV mix policy audit

- Verified Beijing's 2020-revised small-passenger-car quota rules define the new-energy indicator as pure-electric; 2023 quota was 70,000 NEV indicators and 30,000 ordinary indicators.
- Added 2023 replacement-subsidy scope and national statistical NEV-definition sources to distinguish policy and statistical categories.
- Downgraded the national 76.04% BEV stock share from a supposed Beijing central proxy to a national comparator only.
- Added a policy-aware 12-scenario private VKT grid crossing PHEV share (0/5/10/23.96%) and active days (250/300/365), with local Beijing PHEV daily-use evidence.
- Updated parameter register, source register, raw manifest, audit, README and scripts.

- Added the Beijing Public Security Bureau information-disclosure guide, online application navigation, and official request-form page; identified the Traffic Management Bureau as the vehicle-registration record holder.
- Added the 2025 retrospective clarification that ordinary indicators can purchase PHEV/range-extender vehicles and that the policy has existed since 2021.
- Final validation: all eight key CSV/register files have zero malformed rows; policy-aware private VKT grid contains 12 scenarios.

## 2026-11-24 — R5: open-source bus propulsion + corrected pure-BEV monthly VKT

- Replaced inaccessible departmental data-collection/login URL with accessible public operator interview, transport statistics and PDF original Table 4-1.
- Added 2023-04-23 Beijing bus snapshots: 1495 diesel, 6795 natural gas, 15451 mixed new-energy electric-drive; 6 vehicle residual against total 23747, explicitly not assigned.
- Replaced indirect 2023 private BEV monthly mileage 1560.32 with direct observed 1551.6 km/vehicle/month, yielding annualized scenario 18619.2 instead of old 18723.84.
- Added R5 bus VKT pressure scenarios (relative electric-drive annual mileage 0.8,1.0,1.2), keeping mixed electric-drive separate from confirmed BEV.
- Added R5 corrected private propulsion sensitivity, provenance register entries, no-binary status, quality audit and runnable script.
- Flagged legacy BEV-only interpretations of 16832 minus 217 buses and associated VKT/energy totals as superseded/conditional; original files retained.
- No PDF/HTML source bytes archived; no SHA-256 claimed for unarchived sources.

## 2026-11-24 — R9.7D
- Added 30 conditional service cases and six mileage-denominator alternatives; actual PKM remains NA.
- Corrected bus manufacturing audit CSV column order and PHEV production/vehicle-cycle wording. Added regression tests and pipeline steps; figure manifest staging restored. No new Jinhua VKT search.

## 2026-11-24 — R9.7E
- Added nine pre-contest national basic emission factor rows, eight cases and 240 road-exhaust screening results, plus integrated six-scenario environmental matrix with explicit NA for non-exhaust and full life-cycle indicators.
- Integrated generation script and four regression tests in CI. No change to A–D baseline or main branch.

## 2026-11-24 — R9.7F paper audit branch
- Added paired 27-set transfer, 14,580 climate stress sets and 432 exhaust stress sets per pollutant, Jinhua retrospective diagnostic, reversal witness and acceptance matrix. Baseline A–E unchanged. Four regression tests and branch-specific workflow.

## 2026-11-24 — R9.7G-1
- Rebuilt English manuscript with million-city target, explicit activity and stage equations, all six scenarios and mode-specific energy/GWP/exhaust tables, conditional PKM and paired sensitivity, and updated 0.947 kgCO2e/kWh car break-even threshold. No model-input change.
- Rechecked award-paper equation and common-distance diagnostic; differing scopes and CO2/CO2e prevent a quantitative validation claim. Added final figure specification. Prior papers and figures retained; new rendering pending G-2.

## 2026-11-24 — R9.7G-3A
- Reconciled R9.6 versus contest-time evidence, checked Lin2015 Figure 2 and 2024 Table 4-1, corrected prose unit conversion, added independent bus scrapping sensitivity and tests. A–F baseline unchanged; four priority PNGs visually inspected, remaining figure and typeset review pending.

## 2026-11-24 — Final Audit V1 / Audit-01
- Recorded comprehensive ten-dimension audit standard, nine-task sequence and freeze gates; executed A01–A10 with 6 pass, 4 conditional (9.6/12 provisional). Added scope precedence clarification and Q6 interface. Original contest archive unavailable at audit; no model numbers changed. Next Audit-02.

## 2026-11-24 — Audit-01 revision
- User-supplied problem PDF text and p2 visually verified; evidence excerpt and fingerprint recorded. A-001 closed. Rewrote scope to isolate historical 2023 figures and current 2022 anchor. Q1–Q4 explicitly out of scope, Q6 interface only. Deferred issues assigned to Audit-02/03/04/06; 7 pass, 3 conditional, 10.2/12. No computation or figure changes.

## 2026-11-24 — Audit-02
- Audited nine mathematical-framework items; 7 pass, 2 conditional (8.89/10). Independently reconciled reference energy, WTW, production, GWP, NOx and PM2.5; introduced 243 paired propulsion stress sets and all-diesel and urban-numerator alternatives. No baseline changes.
- Corrected manufacturing-register tonne conversion notes (values unchanged); recorded residual-technology synchronization issue for Audit-06. Added structural script and regression tests to existing CI; preserved history and main.

## 2026-11-24 — Audit-03
- Reopened key activity, fuel, UF, production and road evidence; indexed 156 provenance rows and 14 gaps; upgraded operator activity source; separate 18-row historical bus energy stress and CI checks. No baseline numeric change. Conditional 8/12; unresolved specialty issues retained.

- Audit-03 follow-up: added 13-group formula-to-input crosswalk, synchronized operator release dates and inherited issue owners; prior Audit-03 CI 45413722445 passed. No numerical changes.

## Audit-04 — ecological scope
Added 128-cell coverage, 84 wear rows, 132 private-battery LCIA rows and 18 extra-pack stress rows. Baseline unchanged; 7/10 provisional.
