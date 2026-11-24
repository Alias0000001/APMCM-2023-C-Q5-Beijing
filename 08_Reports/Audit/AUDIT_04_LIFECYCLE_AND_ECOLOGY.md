# Audit-04 — Lifecycle and ecological coverage
Reference 3a19b869f1495a5dbf39691896f34428dcda825a. Previous Audit-03 CI 45413984246 passed. Q5 only. A–F baseline unchanged. Additional conditional domains use current activity, not old retrospective annual totals.

## Boundary and source audit
Qiao cradle-to-gate initial pack already included. Xiong 2019 https://www.mdpi.com/1996-1073/12/5/834 §2.3.2 includes factory-to-shop and shop-to-dismantling transport, so current PHEV subtotal is approximate production plus transport, not strictly matched cradle-to-gate. §3.2.6 gives 356.92/628.05 kg GHG per NMC BEV/PHEV over different lifetimes; source assumes battery lasts vehicle life. §3.2.7 includes EOL and avoided metals. No matched ICEV/bus maintenance factors; do not simply add electrified-car-only maintenance to full fleet ranking. Existing Yang physical maintenance and dismantling factors are CO2/other species, not CO2e. Lin bus scrapping separately quantified in G3A. No initial-pack duplication, whole vehicle-cycle plus production duplication, recycling-credit double count, or CO2/CO2e addition. GWP method and production scope remain cross-study proxies. New coverage 8×16=128 cells; status is not share of impacts. Unknown buses allocated, not separately identified; WTW includes fuel supply and operation without separately resolved mass flows.

## Non-exhaust wear: quantitative addition
EEA Transport and environment report 2020 (published 2021), printed p81 Tables A1.4 and A1.5; PDF page 83 visually checked. Generic passenger car brake+tyre 0.0074/0.0138 and surface 0.0041/0.0075 g/km (PM2.5/PM10); bus 0.0316/0.0590 and 0.0205/0.0380. Generic factors are international proxy, not Beijing measured. OECD 2020 https://www.oecd.org/en/publications/non-exhaust-particulate-emissions-from-road-transport_4a4dc6ca-en/full-report/component-7.html Tables 3.6/3.7 PC component rows: sum brake+tyre+road wear, exclude resuspended dust consistently, not published total rows (PM2.5 totals not transparently reconciled with components). Light/heavy BEV100/300 and low/high tyre model, not measured fleet weights. PHEV conventional wear proxy (wear not scaled by UF). Bus BEV same generic factor in reference, .7/1.3 design stress. Add same-species combustion exhaust from current China V proxy. Never sum PM10 and PM2.5. Dust and secondary PM not quantified; no exposure/health inference.
|Case|PM2.5 S0 t|S3 t|Reduction %|PM10 S0 t|S3 t|Reduction %|
|---|---:|---:|---:|---:|---:|---:|
|EEA_equal|30.979|24.149|22.05|51.755|44.751|13.53|
|light_low|30.732|20.168|34.37|51.130|34.703|32.13|
|light_high|30.767|20.737|32.60|51.141|34.893|31.77|
|heavy_low|30.920|23.201|24.96|51.448|39.822|22.60|
|heavy_high|31.027|24.908|19.72|51.519|40.960|20.50|
|bus_low|30.613|23.445|23.41|51.073|43.441|14.94|
|bus_high|31.346|24.853|20.71|52.437|46.062|12.16|
84 rows. S3/S4 exhaust zero but wear nonzero. Report these alongside main results, not hidden in limitations.

## Current private-battery LCIA
Sun et al. 2020 https://doi.org/10.1016/j.jclepro.2020.123006, author preproof https://api.repository.cam.ac.uk/server/api/core/bitstreams/1e70e5ba-4d14-4a3e-bec7-e9a57337725e/content Table 2 printed p10, PDF page 12 visually checked. All 11 rows match ledger (text says 10). ReCiPe Midpoint(H) V1.11; no-credit = material+production, recycling case uses source reported total. Rounded zero is not proof of exact zero. K_s=40*V_BEV/150000+12.8*V_PHEV/150000; capacity proxies from existing Yang ledger, NCM622 hypothetical both modes, existing cross-study mass mismatch retained. No bus chemistry/capacity established, no additive whole-vehicle GWP. 132 rows with two scenarios per indicator; each category separate. S3=S4 since grid changes operation only. Metal depletion rises under source recycling case; not universal recycling benefit. S−1 zero is no private traction packs, not zero ecology.

## Replacement sensitivity and materiality
Use additional 0/.5/1 private pack-equivalents per lifetime only, 124.48 kgCO2e/kWh Sun materials+production; same stress applied to S0 and each scenario; no recycling credit. Bus battery replacement remains NA. 
|Case|S0 kt|S3 kt|Paired reduction %|
|---|---:|---:|---:|
|no_extra_pack|567.789|486.978|14.23|
|half_extra_pack|569.926|518.444|9.03|
|one_extra_pack|572.063|549.910|3.87|
18 rows. Base S0-S3 GWP margin 80.811 kt/year; after one extra pack 22.153 kt/year. Additional omitted differential burden would need to exceed margin to reverse reference comparison, other factors fixed; not an upper bound. Bus scrapping independently computed previously; do not assume all expansions additive without checking boundaries.

## Disposition
A-003 ecological-scope decision addressed with quantified wear and battery categories, not full lifecycle. B-004/C-007 boundary conditional, C-009 partially addressed. Remaining actual upstream VOC/NOx/SO2, matched maintenance/EOL, bus battery, dust, noise, infrastructure and hydrogen residual are not quantified. Noise requires speed and dB/exposure model, not mass sum; infrastructure depends on buildout/utilization; do not claim negligible. Audit-05 numerical verification; Audit-06 coherent residual and joint energy/lifetime/replacement/particle stresses; Audit-07 new figures and latest matrix; Audit-08 language/citations. No final rewrite yet.

## Provisional score
Five equal 2-point criteria: scope/coverage pass 2, physical/characterized separation pass 2, production compatibility conditional 1, materiality/additions conditional 1, comparison/interpretation conditional 1. 7/10. No complete cradle-to-grave or ISO compliance claim; no empirical city validation. 

## Evidence and handoff
EEA Report No 19/2020, Transport and environment report 2020: Train or plane? (2021), printed p81, Tables A1.4/A1.5. Original tables inspected visually. Source factors from EMEP/EEA 2019 Tier 1; use no dust resuspension. Previous battery-capacity proxies 40/12.8 kWh and 150000 km are already in R9_LCI_PARAMETER_LEDGER.csv; this is a hypothetical private battery calculation, not actual battery sales. Audit-04 new issue ledger: AUDIT_04_DEFERRED_ISSUES.csv. First CI 45415319202 passed; generated output commit c37474b. No final manuscript text or images changed; mandatory later integration.
