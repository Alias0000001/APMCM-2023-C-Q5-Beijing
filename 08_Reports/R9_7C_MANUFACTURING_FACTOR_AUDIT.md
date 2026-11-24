# R9.7C — Vehicle and bus manufacturing factor audit

## 1. Scope and conclusion
This task closes the best publicly available pre-contest manufacturing-factor evidence for buses and PHEVs. The result is a source register and annualized scenario ledger, not yet a fully harmonized cradle-to-grave GWP total. Keep private passenger-car production CO2 and bus manufacturing GHG/CO2e in separate columns until the impact metric is harmonized.

## 2. Bus factors — preferred historical base
Lin et al. (2015), Beijing bus LCA, Figure 2 reports raw-material production and vehicle assembly intensities per 1,000 passenger-km; Table 5 supplies effective passengers and a 400,000-km lifetime. Derived per-bus factors:
- CDB diesel: (2.25+0.27) ×42.5×400,000/1,000 = 42.840 tCO2e/bus.
- NGB natural gas: (2.50+0.30) ×40.5×400,000/1,000 =45.360 tCO2e/bus.
- DHEB diesel hybrid: (2.76+0.33) ×37.5×400,000/1,000 =46.350 tCO2e/bus.
- BEB: (3.06+0.40) ×34.5×400,000/1,000 =47.748 tCO2e/bus.
Amortized intensities are 107.10, 113.40, 115.875 and119.37 gCO2e/vehicle-km, respectively. Raw material and assembly only; scrap/EOL is deliberately excluded. This is a 2011–2014-era Beijing technology proxy, not 2023 measured manufacturing data. It is more useful than the old R9.3 material-share-only table because it provides an actual manufacturing-stage impact result.

## 3. Independent bus boundary cross-check
Ying, Wu & Yang (2018), Hangzhou, reports raw-material production/processing CO2 of 120.054 t for diesel bus and213.457 t for BEV, plus1.580 t assembly for each. At 950,000 lifetime km this implies 128.036 and226.355 gCO2/vehicle-km. These are CO2-only, not CO2e, and are not combined with the Lin2015 GWP factors. The paper assumes battery replacement once, but the reported 14.713t per battery set and 88.280t lifecycle battery-production total do not reconcile transparently; use as a high-side structural boundary sensitivity only, not the base factor. The study's full life-cycle totals (1103.237t BEV;1401.319t diesel) also include operating energy and other stages and must not be added to our R9.7B operation results.

## 4. PHEV and private-car manufacturing factors
### 4.1 Matched CO2 production factors: Yang et al. (2021)
The source reports production-stage CO2 intensities of BEV 81–103g/km and PHEV74–90g/km; these are CO2, not CO2e. With the study's 150,000km functional unit:
- BEV midpoint92g/km =13.80tCO2/vehicle (range12.15–15.45t).
- PHEV midpoint82g/km =12.30tCO2/vehicle (range11.10–13.50t).
- The paper states BEV production is about133% and PHEV about119% of ICEV production. ICEV midpoint is inferred from the two ratios: [(92/1.33)+(82/1.19)]/2 =69.04g/km =10.356tCO2/vehicle. The common implied interval is 9.328–11.345t. This is a derived estimate, not a directly tabulated ICEV factor.
These factors provide a complete matched three-technology production CO2 set. The battery is already included; do not add R9.3 battery GWP or another whole-vehicle factor.

### 4.2 Independent GWP/CO2e alternatives
- Qiao et al. (2017) reports cradle-to-gate GWP: ICEV 9.985tCO2e/vehicle; BEV-NMC15.005t; BEV-LFP15.174t. The BEV totals already include the initial traction battery.
- Xiong et al. (2019), Table/section 3.2, production-only contributions sum to BEV-LFP9.516t, BEV-NMC11.518t, PHEV-LFP7.652t and PHEV-NMC8.670tCO2e/vehicle (body + battery + fluids + assembly + transport). Maintenance and EOL excluded. It has no ICEV comparator.
- Peng et al. (2023), Energy 282, issue date 1 Nov 2023, is eligible by the contest cutoff. Its abstract reports vehicle-cycle (not manufacturing-only) GWP of BEV13.533–15.445t and PHEV11.572–12.186t per vehicle. Use only as a whole-vehicle-cycle cross-check, never add it to production factors.

The above sources do not support a single universal factor. Differences reflect vehicle specification, battery chemistry and boundary. Preserve parallel factor sets; do not average incompatible CO2 and CO2e values or sum a battery factor twice.

## 5. Annualized city scenarios
For passenger cars, Yang2021 matched production CO2 factors are amortized over 150,000km. For buses, Lin2015 CO2e manufacturing factors are amortized over400,000km. This is a steady-state annualized replacement burden:
M_annual = sum_k(VKT_k/L_k × M_k).
It is not the actual number of new vehicles manufactured in the target calendar year.

| Scenario | Private production CO2 kt/y (base) | Range kt/y | Bus manufacturing GHG ktCO2e/y |
|---|---:|---:|---:|
| S-1 | 130.814 |117.922–143.453|5.057|
| S0 |133.966|120.538–147.161|5.245|
| S1 |133.966|120.538–147.161|5.377|
| S2 |174.419|153.564–195.273|5.245|
| S3 |174.419|153.564–195.273|5.377|
| S4 |174.419|153.564–195.273|5.377|

Private column is CO2-only; bus column is CO2e. They are intentionally not added into a single total. S4 has the same manufacturing burden as S3 because it changes only electricity supply. All scenario class VKT is preserved; the 6 unclassified bus units' VKT is allocated by the diesel:gas count ratio for manufacturing proxy purposes only.

## 6. Key findings and modelling implications
1. Passenger-car manufacturing can be a substantial annualized burden because the city has a large private-car VKT base. Under the Yang2021 production CO2 proxy, moving from S0 to full BEV increases annualized private production CO2 by about40.45kt/y. This is not an immediate one-year fleet replacement pulse; it is the steady-state burden associated with vehicle replacement over lifetime mileage.
2. Bus manufacturing increases modestly under the Lin2015 proxy when moving from S0 to all BEV buses: about0.132ktCO2e/y. The 2018 Hangzhou boundary alternative implies a much larger per-km BEV manufacturing factor, so bus manufacturing uncertainty deserves a dedicated sensitivity, not a single point estimate.
3. PHEV manufacturing cannot be left blank. Yang2021 supplies a matched production CO2 range; Xiong2019 provides a separate production-only GWP estimate. Retain both, with their impact metric and boundaries explicit.
4. Do not add R9.3 NCM622 battery manufacturing to Qiao2017, Yang2021 or Xiong2019 whole-vehicle production factors where battery production is already included.
5. Do not combine private CO2 with bus CO2e or with R9.7B WTW CO2e until a harmonized impact indicator is selected. A full model result should show CO2 and GWP consistently or keep parallel ledgers.

## 7. Reproduction and tests
Run:
- python 06_S0_Calculation/r9_7a_activity_scenarios.py
- python 06_S0_Calculation/r9_7b_energy_wtw.py
- python 06_S0_Calculation/r9_7c_manufacturing.py
- python -m unittest discover -s tests -v

The script writes three CSV outputs. Regression tests check six scenarios, nonnegative burdens, S3=S4 manufacturing, bus VKT allocation and the separate CO2/CO2e ledger rule. GitHub Actions is configured to run these modules and tests on this branch only.
