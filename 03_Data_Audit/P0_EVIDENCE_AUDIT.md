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

The local Beijing 2021 PHEV study reports city-level average daily VKT for a seven-city PHEV sample, including Beijing (47.1 km/day). The project retains the Shanghai 2018 GPS private-PHEV annual-window mean of 14,774.95 km from a prior table extraction as a provisional central proxy, with Q1 7,333 km, median 12,648 km, and Q3 19,373 km for sensitivity. The current live text extraction verifies the 2018 GPS sample (700 vehicles obtained; 668 retained) but does not expose the exact 14,774.95 mean; re-open Table 2/image before final model freeze.

Decision: PHEV VKT remains a cross-city proxy, not a Beijing 2023 observation. The Beijing daily-distance study is a reasonableness cross-check only; do not multiply a daily mean by 365 without confirming its day denominator.

### A5. BEV/PHEV stock split

The national 2023 NEV stock contained 15.52 million BEVs out of 20.41 million NEVs, i.e. 76.04% BEV and 23.96% non-BEV NEV (including PHEV and fuel-cell vehicles). This is retained only as a national comparator, not a central proxy for Beijing. Beijing's 2020-revised quota rules (in force during 2023) define the new-energy small-passenger-car indicator as pure-electric; the 2023 quota allocated 70,000 new-energy indicators and 30,000 ordinary indicators. PHEVs may be registered under ordinary indicators. This policy distinction makes the national stock mix a weak local proxy. The exact statistical classification of Beijing's 528,000 private new-energy passenger cars is still unverified.

The legacy national-mix comparator scenario therefore uses:
- private non-NEV/ICE group: 4,545,000;
- private BEV proxy: 401,491;
- private PHEV proxy: 126,509.

The BEV/PHEV counts remain class-C scenario estimates, not official Beijing cross-tab data.

### A6. ICE/non-NEV VKT residual

To keep the three classes consistent with the all-private-car activity anchor, ICE/non-NEV annual VKT is calculated as:

`D_ICE = (N_private × D_all - N_BEV × D_BEV - N_PHEV × D_PHEV) / N_ICE`

For the legacy 23.96% national-mix comparator case, the implied ICE/non-NEV annual mileage is approximately 9,505 km/vehicle-year. This is a derived balancing estimate, not a directly observed ICE subgroup mean.

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

A Beijing municipal economic-information bureau reply dated 2023-06-19 reports 217 hydrogen fuel-cell buses in the Beijing bus industry, operated by Beijing Bus Group (5 earlier demonstration vehicles plus 212 Winter Olympics buses).

The following structure estimate assumes that the report's 94.7% clean-energy + new-energy share uses the same 23,385-vehicle denominator as the historical public-bus table. The report summary does not explicitly print that denominator, so the inferred clean-energy and other counts are conditional, not official counts. Under that assumption:
- new-energy buses: 16,832 (reported);
- hydrogen buses: 217 (official snapshot; date 2023-06-19);
- non-hydrogen new-energy buses: 16,615 (derived; treated as BEV/electric-drive proxy, pending exact year-end cross-tab; assumes no H2 additions after 2023-06-19);
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

It also contains annual energy-consumption fields for gasoline, diesel, CNG, LNG, hydrogen, and electricity. The publicly available PDF is a blank reporting template; the populated values are not shown. The reporting scope is all urban public-transport operating enterprises in Beijing. The reporting directory specifies submission by 2024-03-15 through the Beijing Department Data Sharing Collection Platform: http://43.254.24.235:9999/user/login. Codes 3–9 are diesel, CNG, LNG, hybrid, trolleybus, pure electric, and hydrogen vehicle counts; codes 20–25 are gasoline, diesel, CNG, LNG, hydrogen, and electricity consumption. It contains only total public-bus mileage rather than VKT by fuel type. Obtaining the completed form can close the fleet-count and energy-use gaps, but a separate operator odometer/dispatch extract is still needed for propulsion-specific VKT.

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


## E. Publication-time eligibility

The current P0 baseline is a retrospective 2023 reconstruction. Several 2023-observation inputs were published after the competition cutoff of 2023-12-31:
- Beijing 2023 Statistical Communiqué: 2024-03-21.
- 2024 China Major Cities Charging Infrastructure Monitoring Report: 2024 publication, with October 2023 observations.
- Beijing Bus Group 2023 social-responsibility summary: 2024-07-11.
- National 2023 NEV stock composition: first publicly reported in January 2024; the archived annual report is later.
- Beijing 2023 department data-sharing form: published 2024-02-29 and blank in any case.

Pre-cutoff evidence in the current source set includes the 2021 Beijing Transport Development Annual Report (2019/2020 private-car mileage), the 2023-06-19 municipal hydrogen-bus reply (217 H2 buses at that date), the 2023-09 bus-group MTN prospectus (2023H1 public-bus VKT 552 million km), and the 2019 Shanghai private-PHEV GPS study. The 2023H1 bus VKT is not a full-year total.

Do not use the retrospective center scenario as a strict contest-time evidence set. For strict 2023-12-31 reproducibility, build a separate scenario using only pre-cutoff publications and leave post-cutoff 2023 year-end observations in a retrospective appendix.


## F. Round 3 — alternative access routes and substitute evidence (2026-11-23)

### F1. Corrected access route

The previously listed `http://43.254.24.235:9999/user/login` is a departmental reporting/collection backend for reporting organizations, not a public data-download page. It should no longer be presented as the user's public access route.

The Beijing Municipal Transport Commission's official information-disclosure guide provides four application methods: online through the JTW portal, in-person, postal mail and fax. The published contact details are:
- telephone: 010-12328;
- fax: 010-55530733;
- postal address: 北京市通州区达济街6号院3号楼 北京市交通委员会政府信息公开办公室;
- postal code: 101160.
The guide states that the commission generally replies within 20 working days, subject to statutory extension. A request should seek existing records or completed forms, not ask the agency to create a new statistical analysis.

### F2. Pre-cutoff bus activity recovered from the 2023 MTN prospectus

The September 2023 Beijing Public Transport Group MTN prospectus (pre-cutoff) reports:
- 2020: 1.068 billion public-bus vehicle-km and 1.826 billion passenger trips;
- 2021: 1.139 billion vehicle-km and 2.296 billion passenger trips;
- 2022: 0.984 billion vehicle-km and 1.726 billion passenger trips;
- 2023 H1: 0.552 billion vehicle-km and 0.977 billion passenger trips.

The 2023 H1 passenger-trip/VKT ratio is 1.770 trips per vehicle-km. This is a service-intensity indicator only; it is not average passenger occupancy and cannot be substituted for PKM.

The prospectus also reports 2022 full-year costs of 179,238.23万元 for fuel and 52,430.40万元 for 电车电力, and 2023 H1 costs of 82,072.54万元 and 29,434.64万元 respectively. Dividing by the corresponding total bus VKT gives 2023 H1 cost intensities of about 1.487 RMB/vehicle-km for fuel and 0.533 RMB/vehicle-km for 电车电力. These are financial accounting costs, not litres, Nm³, kg or kWh. The 电车电力 boundary is not confirmed as BEV-only. They are cost cross-checks, never LCA energy inputs or emission factors.

### F3. Bus operating time series and derived indicators

The Beijing Bus Group historical-statistics page now exposes a 2020–2025 annual series. The source category is `公共电汽车`; it must not be interpreted as a BEV-only class. For 2023:
- year-end operating vehicles: 23,385;
- annual VKT: 1.151 billion vehicle-km;
- passenger trips: 2.08687 billion;
- derived VKT per year-end vehicle: 49,219.6 km/year;
- derived passenger trips per VKT: 1.8131.

From 2022 to 2023, total VKT increased about 17.0%, passenger trips increased about 20.9%, while year-end operating vehicles decreased about 0.34%. The per-vehicle value uses year-end stock as denominator and is only an approximate intensity, not a fleet-weighted odometer mean.

The 2023 H1 VKT in the MTN prospectus is 47.96% of the 1.151 billion full-year figure from the current operator page. If the two scopes are identical, the implied H2 residual is 599 million km; this is a reconciliation residual, not an independently reported H2 observation.

### F4. Local Beijing PHEV travel sample

The 2021 peer-reviewed PHEV utility-factor study reports a Beijing subsample of 45 PHEVs, 10,372 effective vehicle-days, 488,521 km total distance, mean daily VKT 47.1 km and standard deviation 56.2 km. Seasonal daily means are spring 44.9, summer 55.3, autumn 50.6 and winter 49.3 km.

The study does not state a clear full-year observation window in the accessible article text. Therefore:
- 47.1 km is treated as km per effective vehicle-day, not calendar-day VKT;
- 250/300/365 active-day annualizations (11,775/14,130/17,191.5 km/year) are sensitivity scenarios only;
- none of these values is a Beijing 2023 fleet mean;
- raw telemetry is restricted by the National Monitoring and Management Centre for New Energy Vehicles.

This local historical sample is a stronger geographic cross-check than the Shanghai annual-mileage proxy, but it does not replace a 2023 local VKT observation.

### F5. Additional Beijing open-data routes

1. The official open-data platform exposes a bus-stop dataset with 152,566 records and fields for route name, direction, stop sequence and stop name. It is useful for route topology and service-network reconstruction, but the listed fields do not include coordinates or propulsion, VKT or energy use. Download/API access requires a registered account and user key.
2. The platform also exposes a dataset named `实时公交-公交历史运行轨迹`. Its metadata states 1,000 records, fields including device ID, direction, speed, address, location and timestamp, but no time range or geographic coverage. Crucially, it is listed under synthetic/open data and described as AI-generated by the Beijing Big Data Center. It is suitable only for pipeline/schema testing, not as observed 2023 trajectory or VKT evidence.
3. The platform's help page says that when a dataset is not available, users can submit a data-type request through 互动交流 → 建议增加的数据类型; the platform may coordinate with the source department. This is a separate route from the JTW statutory information-disclosure application.

### F6. Pre-cutoff new-energy bus count cross-check

A Beijing Stock Exchange issuer-disclosure response published 2023-11-06 reports 15,137 existing new-energy buses for Beijing Bus Group. The exact observation date is not stated. It is retained as a pre-cutoff cross-check only; do not divide it by a fleet count from a different date or infer an exact share. The later 2023 year-end social-responsibility figure of 16,832 new-energy buses is retrospective and should remain a separate observation.

### F7. Exact request scope recommended

For a statutory information-disclosure request to the Beijing Municipal Transport Commission, ask for copies or extracts of existing 2023 records:
- completed BMZ04-073-108 entries for pure electric, hydrogen, CNG, LNG, diesel, hybrid and trolleybus operating vehicle counts;
- corresponding already-reported annual electricity, hydrogen, CNG, LNG and diesel consumption;
- any existing propulsion-specific VKT, odometer, dispatch or vehicle-kilometre records for 2023;
- the reporting scope, units, observation date and whether suburban operators are included.

Phrase the request as access to existing records. If the commission does not hold the records, ask it to identify the actual holding department or the applicable public-data request channel.

## G. Round 3 data-use decision

- Admit the 2023 H1 public-bus VKT and passenger trips as pre-cutoff official issuer-disclosure evidence.
- Admit 2020–2022 bus VKT and trips as historical pre-cutoff comparison values from the same prospectus.
- Use the full-year 2023 bus activity series as retrospective data only.
- Use bus operating-cost ratios only as financial reasonableness checks.
- Use Beijing PHEV 47.1 km/effective-day as a historical local sensitivity anchor, never as 2023 annual VKT without an explicit active-day assumption.
- Use open bus-stop data for route topology after obtaining the registered download; do not use synthetic trajectory records as observations.


## H. Private BEV/PHEV mix policy audit — correction to the former central proxy

### H1. Official Beijing policy distinction

The 2020-revised Beijing small-passenger-car indicator rules, published 2020-12-07 and effective 2021-01-01, define `新能源小客车` in the quota system as pure-electric-drive small passenger cars. In 2023, Beijing allocated 70,000 new-energy indicators and 30,000 ordinary indicators. Plug-in hybrids can be purchased under ordinary indicators; the quota categories therefore affect the local composition but do not directly disclose the registered stock split.

The 2023 replacement-subsidy scheme separately defined subsidy-scope new-energy small passenger cars as pure-electric, including range-extenders. National statistical methodology, by contrast, defines NEVs to include BEV, PHEV (including range-extender) and fuel-cell vehicles. These are different administrative/statistical contexts and must not be conflated.

### H2. Correction

The previous calculation treated the national 2023 BEV share of 76.04% as Beijing's central private-NEV composition, producing 401,491 BEVs and 126,509 PHEVs. This is no longer admitted as a Beijing central estimate. It is retained only as a national-mix comparator because:
- Beijing's quota-policy new-energy indicator is pure-electric;
- PHEVs can be registered under ordinary indicators;
- the 2023 statistical bulletin does not publish a BEV/PHEV cross-tab for the 528,000 private new-energy passenger cars;
- the national non-BEV remainder includes fuel-cell vehicles and is not exactly equivalent to PHEV.

The 528,000 stock count remains usable as the aggregate private NEV count, but its local propulsion split remains unknown.

### H3. Policy-aware sensitivity grid

A new 12-scenario grid combines:
- assumed PHEV share within the 528,000 private NEVs: 0%, 5%, 10%, 23.96%;
- Beijing PHEV historical daily mean: 47.1 km per effective vehicle-day;
- assumed active days: 250, 300, 365;
- BEV annualized October 2023 VKT: 18,723.84 km/vehicle-year;
- all-private-car activity anchor: 10,366 km/vehicle-year.

The 0% case is a boundary case, not an assertion that all reported NEVs are BEV. The 5% and 10% cases are low local-mix sensitivities, not observed fleet shares. The 23.96% case is only the national-mix comparator. In every scenario, ICE/non-NEV mileage is a residual calibrated to the all-private-car activity anchor.

For the 300-active-day sensitivity:
- PHEV share 5%: 26,400 PHEVs, 14,130 km/PHEV-year, implied ICE/non-NEV 9,422 km/year;
- PHEV share 10%: 52,800 PHEVs, 14,130 km/PHEV-year, implied ICE/non-NEV 9,448 km/year;
- PHEV share 23.96% comparator: 126,509 PHEVs, 14,130 km/PHEV-year, implied ICE/non-NEV 9,523 km/year.

All these values are sensitivity outputs, not local registration observations. See `02_Cleaned_Data/P0_private_VKT_policy_mix_sensitivity.csv`.

### H4. Model-use decision

- Do not cite 23.96% as Beijing's central BEV/PHEV share.
- Keep 528,000 as aggregate private new-energy passenger-car stock, subject to its statistical classification.
- Use the new 12-scenario grid for robustness testing.
- Request the 2023 private passenger-car stock cross-tab by BEV, PHEV/range-extender and fuel-cell from the Beijing traffic-management/statistics authority through the government information-disclosure route.
- Until that cross-tab is obtained, do not report a single local BEV/PHEV fleet split as measured fact.


### H5. Private vehicle registration-data request route

The likely record-holding authority is the Beijing Public Security Traffic Management Bureau, which is responsible for motor-vehicle registration. Its parent agency, the Beijing Public Security Bureau, provides a separate government-information-disclosure route:
- guide: https://gaj.beijing.gov.cn/zfxxgk/zfxxgkzn/index.html
- online application: Beijing Public Security Bureau homepage → 警务公开 → 依申请公开网页申请;
- application form page: https://gaj.beijing.gov.cn/wsgs/bsbg/qita/202112/t20211231_2580778.html
- telephone 010-82097828; fax 010-82097838;
- mail: 北京市东城区前门东大街9号, postcode 100740.

The application should request aggregated private small-passenger-car stock by fuel/power type as of 2023-12-31, not owner-level data. Ask the PSB to route the request to its Traffic Management Bureau / Vehicle Management Office if the records are held there.

A 2025 official clarification states that ordinary small-passenger-car indicators can be used to purchase plug-in hybrid (including range-extender) and fuel-cell passenger cars, and says this practice has existed since 2021. This is a post-cutoff clarification of the policy path, not a 2023 registration count. Source: https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/202509/t20250909_4194533.html.
