# R9.6 — Figure regeneration, bus manufacturing, PKM and R7 energy-boundary audit

Date: 2026-11-24  
Branch: `work/r96-figures-energy-audit-20261124`  
Reference year: 2023; post-2023 publications are retrospective evidence only.

## Executive decisions

1. Correct the private-BEV energy-intensity row from 15.2 to **16.0 kWh/100 km**. The 15.2 value in Table 4-1 of the 2024 China Major Cities Charging Infrastructure Monitoring Report belongs to the taxi passenger-car row, while the private passenger-car row is 16.0.
2. Keep the electric-bus intensity at **62.6 kWh/100 km**. Its monthly distance and charging-energy fields reproduce that value.
3. The charging report does not identify whether energy is metered at the grid input, charging equipment output, or battery discharge. Keep the input as reported charging-energy-per-distance and do not silently add charging losses. A separate 90%, 92%, and 95% charging-efficiency sensitivity is recorded.
4. A defensible **historical Beijing bus manufacturing proxy** can be derived from Lin et al. (2015), but it is not a 2023 observed factor. Keep it separate from the current physical-emission track and the private-car two-stage GWP track until the system boundaries are harmonized.
5. No public 2023 Beijing city-bus-only passenger-kilometre total was found. Use VKT as the primary functional unit. Do not derive observed PKM by multiplying boardings by an arbitrary average trip length.

## 1. R7 private-BEV energy row correction

Source: *2024 China Major Cities Charging Infrastructure Monitoring Report*, Table 4-1, observation month 2023-10, PDF: https://file.jgvogel.cn/125/upload/resources/file/574928.pdf

- Private passenger-car monthly distance: 1,551.6 km.
- Private passenger-car monthly charging energy: 248.7 kWh.
- Recomputed intensity: 248.7 / 1,551.6 × 100 = 16.0209 kWh/100 km, reported as 16.0.
- Taxi passenger-car row reports 15.2 kWh/100 km. This appears to have been misassigned to the private-BEV coefficient in earlier R7/R9 scripts.
- Electric-bus monthly distance: 3,770.8 km.
- Electric-bus monthly charging energy: 2,361.3 kWh.
- Recomputed intensity: 2,361.3 / 3,770.8 × 100 = 62.6234 kWh/100 km, reported as 62.6.

For the 1-million-person representative city, private-BEV VKT is 427,275,629.975 km/year. Moving from 0.152 to 0.160 kWh/km increases private-BEV electricity by:

`427,275,629.975 × 0.008 = 3,418,205.040 kWh/year`.

The R7 total electricity therefore rises from approximately 83.9065 million to 87.3247 million kWh/year, before any separate charging-loss sensitivity. All downstream R9.1–R9.5 outputs must be regenerated from the corrected input.

### Meter boundary

The source table reports monthly charging energy and a derived/rounded per-100-km consumption. It does not specify the physical meter boundary. Therefore:

- Do not call the number definitively battery-side.
- Do not call it definitively grid-side.
- Do not apply an extra charging-loss multiplier in the base case without evidence.
- Retain a separate battery-side interpretation sensitivity: grid input = reported value / charging efficiency, with 0.90, 0.92 and 0.95 illustrative efficiencies.

## 2. Historical Beijing bus manufacturing proxy

Source: Lin Xiaodan et al. (2015), *基于LCA的北京市公交车节能及温室气体减排潜力分析*, Acta Scientiae Circumstantiae 35(2):576–584. Article: https://html.rhhz.net/hjkxxb/html/20140430001.htm

The paper uses 1000 passenger-km as its service unit. Figure 2 reports raw-material and vehicle-assembly GWP intensities; Table 5 reports effective passengers per bus and a 400,000-km bus-life assumption.

Derived factor:

`manufacturing GWP per bus = (raw-material + assembly/distribution GWP per 1000 PKM) × effective passengers × lifetime vehicle-km / 1000`.

| Bus technology | Raw material | Assembly/distribution | Effective passengers | Derived manufacturing factor |
|---|---:|---:|---:|---:|
| Diesel | 2.25 | 0.27 | 42.5 | 42.84 t CO2e/bus |
| Natural gas | 2.50 | 0.30 | 40.5 | 45.36 t CO2e/bus |
| Diesel hybrid | 2.76 | 0.33 | 37.5 | 46.35 t CO2e/bus |
| Battery electric | 3.06 | 0.40 | 34.5 | 47.748 t CO2e/bus |

The first two numeric columns are kg CO2e per 1000 PKM. The derived values are per bus over the assumed 400,000-km life. Vehicle scrapping is a separate stage and is not included in the manufacturing factor.

These are 2011–2014-era Beijing technology proxies published in 2015. They are suitable for a clearly labelled historical proxy/sensitivity, not as 2023 observed fleet factors. The 2024 Harbin 12-m bus study is a retrospective cross-check only; its vehicle-cycle values differ between Figure 6 and Table 15 and should not be substituted without reconciling the internal discrepancy.

## 3. 2023 actual bus PKM audit

Beijing Bus Group's 2023 operator statistics expose two columns. The R7 bus scope uses the Public Electric Bus column:

- 1.151 billion vehicle-km.
- 2.08687 billion passenger boardings.

The same page's Total column reports 1.47566 billion vehicle-km and 2.14368 billion passenger boardings. These are retained as scope cross-checks, not substituted into the R7 public-electric-bus activity anchor.

Their ratio is 1.813 passenger trips per vehicle-km. It is not passengers aboard per kilometre and not passenger-km.

The 2023 Beijing statistical report provides overall passenger turnover by transport mode, but it does not expose a separate city-bus PKM value in the table reviewed. The road passenger-turnover item is not a city-bus-only measure and must not be assigned to buses.

Lin et al. (2015) cite approximately 32.85 billion passenger-km for Beijing conventional buses around 2017. This is historical and not a 2023 observation. A 2023 smart-card OD study is useful method evidence, but the paper does not publish a citywide 2023 bus-only PKM total.

Recommended treatment:
- Primary comparison: vehicle-km.
- Secondary comparison: historical-PKM proxy only, with year and occupancy assumptions visible.
- Actual 2023 PKM: keep NA until the bus operator or transport authority supplies AFC OD or route-level passenger-turnover records.

## 4. Figure inventory

R9.6 regenerates figures from repository CSV inputs rather than embedding manually copied arrays:

- Figures 3, 5, 6, 7 and 8: revised existing figures.
- Figure 9: lifecycle data-coverage matrix.
- Figure 10: five-pollutant partial physical inventory.
- Figure 11: grid × lifetime factorial heatmaps.
- Figure 12: battery-only ReCiPe recycling profile.
- Figure 13: historical Beijing bus manufacturing proxy.
- Figure 14: R7 electricity-meter-boundary schematic.
- Figure 15: 2023 bus PKM evidence-status chart.

All partial results and historical proxies are explicitly labelled. Figures 13–15 are evidence/limitations figures, not claims of a complete 2023 citywide LCA.

## 5. Test execution without Work

This branch adds a GitHub Actions workflow and standard-library Python tests. The intended validation sequence is:

1. Regenerate R7.
2. Regenerate R9.3 battery and historical-bus modules.
3. Regenerate R9.1/R9.2 foreground, passenger-car and bus-use modules.
4. Regenerate R9.4 and R9.5 tables.
5. Generate SVG figures from CSVs.
6. Run unit tests and XML parsing on every SVG.
7. Commit regenerated CSV/SVG outputs back to this branch only.

If GitHub Actions is disabled or the linked GitHub App cannot write workflow results, the same commands can be run locally from the repository root with Python 3.11+; no third-party package is required for the audit/generator/tests. See the accompanying manual runbook in the chat response.
