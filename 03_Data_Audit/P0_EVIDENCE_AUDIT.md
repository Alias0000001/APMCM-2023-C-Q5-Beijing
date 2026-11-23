# P0 evidence audit — Beijing private-car VKT and bus propulsion

Audit date: 2026-11-23

## A. Private passenger cars

### A1. Official fleet counts

The 2023 Beijing Statistical Communiqué reports 5.073 million private passenger vehicles and 528,000 new-energy passenger vehicles. The implied non-NEV remainder is 4.545 million.

Decision:
- 5.073 million is admitted as the official private passenger stock.
- 528,000 is admitted as aggregate private passenger NEV stock.
- 4.545 million is a derived non-NEV remainder, not a direct ICE-only count.
- The communiqué does not publish a Beijing private-passenger BEV/PHEV split.

### A2. 2023 activity anchor

The 2024 China Major Cities Charging Infrastructure Monitoring Report (China Academy of Urban Planning & Design, NEV National Big Data Alliance and partners) reports a 2023 private-car daily travel intensity of 28.4 vehicle-km/day. The model uses 28.4 × 365 = 10,366 km/vehicle-year as an all-private-car annual activity anchor.

This conversion assumes the reported daily intensity is a calendar-day average per private car. It is a derived annualization, not a separately published odometer annual mean. The 2021 Beijing Transport Development Annual Report provides a local historical cross-check: 2019 sample mean 12,168 km/year and 2020 sample mean 10,382 km/year. The 2020 result was affected by COVID-era travel conditions.

### A3. Private BEV VKT

The 2024 China Major Cities Charging Infrastructure Monitoring Report gives the 2023-10 private-passenger BEV charging statistics:
- monthly charging sessions: 9.2;
- average driving distance per charging session: 169.6 km.

Derived monthly distance:
`9.2 × 169.6 = 1,560.32 km/month`

Derived annualized distance:
`1,560.32 × 12 = 18,723.84 km/vehicle-year`

This is a one-month (October 2023) annualization based on a BEV charging sample, not a full-year odometer observation. The 2022 comparison is 8 sessions/month × 129 km/session = 1,032 km/month, or 12,384 km/year annualized.

### A4. Private PHEV VKT

The local Beijing 2021 PHEV study reports city-level average daily VKT for a seven-city PHEV sample, including Beijing (47.1 km/day). The project retains the Shanghai 2018 GPS private-PHEV annual-window mean of 14,774.95 km as the central annual proxy, with Q1 7,333 km, median 12,648 km, and Q3 19,373 km for sensitivity.

Decision: PHEV VKT remains a cross-city proxy, not a Beijing 2023 observation. The Beijing daily-distance study is a reasonableness cross-check only; do not multiply a daily mean by 365 without confirming its day denominator.

### A5. BEV/PHEV stock split

The national 2023 NEV stock contained 15.52 million BEVs out of 20.41 million NEVs, i.e. 76.04% BEV and 23.96% non-BEV NEV (mainly PHEV, with fuel-cell vehicles a small component). This national stock share is used only as the central proxy for Beijing's private NEV mix. Low/high PHEV shares of 10% and 30% are tested because Beijing's purchase-quota rules and local vehicle mix may differ from the national stock.

The central model therefore uses:
- private non-NEV/ICE group: 4,545,000;
- private BEV proxy: 401,491;
- private PHEV proxy: 126,509.

The BEV/PHEV counts remain class-C scenario estimates, not official Beijing cross-tab data.

### A6. ICE/non-NEV VKT residual

To keep the three classes consistent with the all-private-car activity anchor, ICE/non-NEV annual VKT is calculated as:

`D_ICE = (N_private × D_all - N_BEV × D_BEV - N_PHEV × D_PHEV) / N_ICE`

For the central 23.96% PHEV-share case, the implied ICE/non-NEV annual mileage is approximately 9,505 km/vehicle-year. This is a derived balancing estimate, not a directly observed ICE subgroup mean.

## B. Public buses

### B1. Total fleet and activity

The Beijing Public Transport Group historical table reports for 2023:
- source category 公共电汽车: 23,385 operating vehicles;
- annual operating mileage: 1.151 billion vehicle-km;
- passenger trips: 2.08687 billion.

The 1.151 billion km is a mixed-fleet total. It must not be labelled BEV-only. The 2023 MTN prospectus from the same operator independently reports 2023H1 public electric-bus VKT of 552 million km (and 2020–2022 full-year totals of 1.068, 1.139, and 0.984 billion km), supporting the operator-scope interpretation of the historical series; it does not provide the full-year 2023 fuel-specific split.

### B2. New-energy and clean-energy structure

The Beijing Bus Group 2023 social-responsibility report states:
- new-energy buses at year end: 16,832;
- clean-energy plus new-energy buses: 94.7% of the bus fleet.

A Beijing municipal economic-information bureau reply dated 2023-12-07 reports 217 hydrogen fuel-cell buses in the Beijing bus industry, operated by Beijing Bus Group (5 earlier demonstration vehicles plus 212 Winter Olympics buses).

A provisional structure estimate is therefore:
- new-energy buses: 16,832 (reported);
- hydrogen buses: 217 (official snapshot; date 2023-12-07);
- non-hydrogen new-energy buses: 16,615 (derived; treated as BEV/electric-drive proxy, pending exact year-end cross-tab);
- clean-energy aggregate: approximately 5,314, derived from round(23,385 × 94.7%) - 16,832;
- other buses: approximately 1,239, residual.

The clean-energy aggregate is not split into CNG and LNG. The residual is not labelled diesel-only; it may include diesel, hybrid, trolleybus, or other categories. The 94.7% share is rounded, so the inferred counts are approximate.

### B3. Official fuel-type reporting form

The 2023 Beijing Department Data Sharing System form BMZ04-073-108 explicitly defines the following public-transport vehicle count categories:
- diesel;
- compressed natural gas (CNG);
- liquefied natural gas (LNG);
- hybrid;
- trolleybus;
- pure electric;
- hydrogen.

It also contains annual energy-consumption fields for gasoline, diesel, CNG, LNG, hydrogen, and electricity. The publicly available PDF is a blank reporting template; the populated values are not shown. The reporting scope is all urban public-transport operating enterprises in Beijing. It contains fuel-type vehicle counts and fuel/electricity consumption, but only total public-bus mileage rather than VKT by fuel type. Obtaining the completed form can close the fleet-count and energy-use gaps, but a separate operator odometer/dispatch extract is still needed for propulsion-specific VKT.

### B4. BEV bus VKT estimate

The 2024 China Major Cities Charging Infrastructure Monitoring Report reports for October 2023:
- average monthly VKT per electric public bus: 3,770.8 km;
- average monthly electricity: 2,361.3 kWh;
- electricity intensity: 62.6 kWh/100 km.

Annualized per-vehicle VKT:
`3,770.8 × 12 = 45,249.6 km/vehicle-year`

Estimated BEV/electric-drive VKT:
`16,615 × 45,249.6 = 751.8 million vehicle-km/year`

Compared with the official mixed-fleet total of 1.151 billion km, this is approximately 65.3%. The remaining 399.2 million km is retained as an unallocated non-BEV residual. It is not divided among hydrogen, CNG, LNG, diesel, hybrid, or trolleybus because no compatible propulsion-specific VKT table has been published in the sources reviewed.

This is an estimate combining a reported fleet count and an October sample mean annualized to 12 months; it is not a measured annual BEV odometer total.

Using the same October electric-bus sample, monthly electricity is 2,361.3 kWh/vehicle and the reported intensity is 62.6 kWh/100 km. Annualized fleet electricity is estimated as 16,615 × 2,361.3 × 12 = 470.8 GWh/year. This is also a one-month annualization and must be checked against vehicle-side/grid-side meter boundaries before emissions accounting.

## C. What remains unavailable

1. Official Beijing 2023 private passenger BEV/PHEV registration cross-tab.
2. Full-year 2023 private BEV and PHEV VKT by propulsion type from the same sample/method.
3. Official populated BMZ04-073-108 fuel-type vehicle counts and annual fuel/electricity consumption.
4. 2023 public-bus VKT separately for pure electric, hydrogen, CNG, LNG, diesel, hybrid, and trolleybus.
5. Exact CNG versus LNG bus count and energy consumption.

## D. Data request route

Request from Beijing Municipal Transport Commission / Beijing Department Data Sharing Platform:
- BMZ04-073-108 table for reporting year 2023, including codes 1–9 and 20–25;
- monthly or annual vehicle-km by fuel type if available;
- the reporting enterprise scope and whether values cover all city public-transport operators;
- corresponding energy consumption (litres, Nm³, kg, kWh) and meter boundary.

For private passenger cars, request the Beijing Vehicle Management / traffic management authority's 2023 private passenger registration counts by energy type, plus the city traffic survey's annual VKT by vehicle type. If no public disclosure is possible, retain the current proxy scenarios rather than inventing local counts.
