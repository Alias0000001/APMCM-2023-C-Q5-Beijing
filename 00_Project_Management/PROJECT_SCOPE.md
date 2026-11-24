> **现行优先口径（Audit-01, 2026-11-24）**：正式竞赛时点模型以R9.7A–F为准，2022年北京全市常住人口21,843,000、目标1,000,000代表性城市，缩放1,000,000/21,843,000；2023年4月公交快照及其他赛题截止（2023-11-27 09:00北京时间）前公开资料为代理。金华为回顾性迁移诊断，不取代北京参考系统。下文原2023人口21,858,000及相关统计、缩放属于R7–R9.6回顾性历史口径，禁止用于现行主计算；实际PKM仍NA，条件性服务比较见R9.7D。当前S−1为汽油私车、柴油/天然气公交比例，全柴油替代待Audit-02/06审查。详细审核见08_Reports/Audit/AUDIT_01_TASK_COMPLIANCE.md。原历史记录保留。

# Project scope and frozen conventions

## 1. Research objective

Evaluate the environmental implications of urban passenger-transport electrification for APMCM 2023 C, Problem 5, using Beijing as the real-city anchor and scaling the relevant activity indicators to the problem's 1,000,000-person representative city.

This is a data-preparation and reproducibility workspace. The presence of a parameter in a register does not mean the S0 calculation is complete.

## 2. Geographic and temporal scope

- **Anchor geography:** Beijing Municipality, unless a source explicitly states central urban area or an operator-specific boundary.
- **Reference year:** 2023 for the core city statistics.
- **Target population:** 1,000,000.
- **Retrospective publications:** a source published after 2023 may be used to describe a 2023 observation, but its publication date must remain visible. Example: the official 2023 provincial electricity CO2 factor was published on 2025-12-31.

Municipality-wide statistics must not silently be relabelled as central-city statistics. Historical central-urban-area observations are retained only as separate evidence.

## 3. Vehicle scope

### Private passenger vehicles

The 2023 Beijing Statistical Communiqué reports 5.431 million private automobiles, of which 5.073 million are passenger vehicles; it reports 528,000 new-energy passenger vehicles within the private-automobile category. These categories must remain distinct.

The published count does not provide a private-passenger BEV/PHEV cross-tab. Do not derive one by applying the city-wide new-energy share to private vehicles.

### Public buses

The Beijing Public Transport Group historical table uses the source category label “公共电汽车”. Preserve this label. It is not sufficient evidence to classify every vehicle as a battery-electric bus (BEV), nor does it provide a propulsion-type split. Bus fleet counts, vehicle-kilometres, passenger trips, and operator-wide totals must be stored separately.

### Exclusions pending evidence

Taxi, ride-hailing, freight vehicles, rail, and other modes are not silently merged into the private-passenger or public-bus activity totals.

## 4. Functional units and activity measures

- City-system output: annual total for a representative city of 1,000,000 residents.
- Vehicle activity: vehicle-kilometres (VKT).
- Passenger service: passenger-kilometres (PKM), only when a compatible passenger-distance measure is available.

Passenger trips are not PKM. Convert trips to PKM only with a supported average trip distance or direct passenger turnover statistic.

## 5. Population scaling

The baseline scaling factor is:

s = 1,000,000 / 21,858,000.

For an extensive count or annual activity total with a compatible geographic boundary:

X_1m = s × X_Beijing.

This is a transparent linear baseline, not a claim that transport demand is universally linear in population. It must be accompanied by sensitivity analysis and a limitation statement. Do not scale intensity factors (for example, kg CO2/kWh).

## 6. Environmental accounting

- Distinguish vehicle-stock electrification share from VKT electrification share.
- Keep local road emissions separate from full life-cycle burdens; do not add the same operation emissions twice.
- Distinguish CO2 from CO2e.
- Distinguish grid-average operational electricity factors from full life-cycle electricity factors.
- Match energy and emission factors to the same vehicle technology, geography, year, and system boundary.
- Keep vehicle manufacturing, battery manufacturing, electricity/fuel supply, operation, maintenance, and end-of-life boundaries explicit.

## 7. Evidence classes

- **A — official observation/statistic:** official statistical release or administrative/official operator statistics.
- **B — literature/institutional evidence:** peer-reviewed article or institutional study.
- **C — derived estimate/proxy:** calculation from A/B evidence or transfer from another geography/year.
- **D — assumption/scenario:** explicit modelling assumption, never described as observed fact.

Each value must also carry a verification state: verified, carried forward pending re-open, provisional, quarantined, or missing.

## 8. Admission rule

A parameter is eligible for the baseline only when its definition, unit, geography, year, population, and boundary are compatible with the model equation. Otherwise it remains a cross-check, sensitivity input, proxy, or data gap.
