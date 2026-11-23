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
- Added reproducible round-3 script, three cleaned datasets, parameter/source/raw manifests, audit and Chinese round report.
