# R9.7F — Paired city-transfer and uncertainty sensitivity

Beijing remains the empirical anchor; inference target is a hypothetical million-resident city. Transfer E(s)=g*m*E_private(s)+b*E_bus(s), where g is ownership density, m annual mileage, b bus VKT intensity. Each tested at 0.8/1/1.2 (27 sets), not probability bounds. No duplicate spatial multiplier; every reduction paired with its own S0. Strict baseline uses 2022 pre-contest Beijing activity; exclude retrospective Jinhua observations.

Jinhua R7.1 diagnostic g=1.171038, b=0.646917 (later-published 2023 observations, provincial passenger-stock proxy, unmatched operator service areas), m=0.8/1/1.2. Ratios use earlier retrospective Beijing reference, not re-estimated against 2022 anchor; external stress only. No actual Jinhua VKT imputed.

Nested climate stress: 27 transfer sets × 2 mileage-denominator interpretations (1 or 1/0.461) × 15 existing energy cases × 2 manufacturing factor sets × 3 car lifetimes (100k/150k/200k) × 3 bus lifetimes (300k/400k/500k) = 14580 matched six-scenario sets. Production scaled by reference lifetime/new lifetime, no duplicate battery burden. Energy cases are existing one-at-a-time cases, not exhaustive joint energy grid. Extreme products of ownership, mileage and denominator are stress, not observed urban ranges. Exhaust: 27 × 2 × 8 cases = 432 per pollutant; distinct from upstream and non-exhaust.

|Scenario|GWP min/max kt/year|paired reduction min/max %|
|---|---:|---:|
|S-1|308.75–2185.10|-6.49–-0.28|
|S0|298.34–2138.68|0.00–0.00|
|S1|290.91–2127.62|0.33–3.82|
|S2|240.05–1866.48|-6.46–33.36|
|S3|230.95–1857.02|-6.01–33.77|
|S4|152.13–1377.11|19.88–57.36|
Strict ranking S4<S3<S2<S1<S0<S-1 holds in 14223/14580 climate sets. Bus priority gives greater NOx reduction in 337/432 sets, private priority in 95/432; PM2.5 1/432 and 431/432. Design-grid frequencies, not probabilities. S3/S4 covered combustion exhaust zero, not total road pollution.

Jinhua diagnostic m=1:
- S-1: 658.570 ktCO2e/year; reduction -2.24%
- S0: 644.119 ktCO2e/year; reduction 0.00%
- S1: 638.126 ktCO2e/year; reduction 0.93%
- S2: 560.335 ktCO2e/year; reduction 13.01%
- S3: 554.342 ktCO2e/year; reduction 13.94%
- S4: 389.953 ktCO2e/year; reduction 39.46%
Activity-transfer scenarios with Beijing technical intensities, not actual Jinhua emissions. R9.7D equal-PKM stress remains separate; no mode substitution. Partial GWP excludes unquantified stages.

Reproduce after A–E: python 06_S0_Calculation/r9_7f_transfer.py. Base grid 162 rows; retrospective diagnostic 18 rows; paired envelopes 36 rows. Independent JS calculation before commit.
