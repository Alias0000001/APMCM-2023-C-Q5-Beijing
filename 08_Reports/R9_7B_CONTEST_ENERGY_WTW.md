# R9.7B — Pre-contest energy and WTW operating screening

## Scope
Input: R9.7A fixed annual VKT (2022 activity proxy, 2023 April structure). Target one million inhabitants. All empirical input publications used in the calculation predate the November 2023 competition; assumptions are scenario values. This is an operational fuel/electricity life-cycle GHG (WTW) calculation, not tailpipe CO2, nor complete vehicle LCA. It does not include vehicle manufacture, maintenance, end of life or local non-GHG pollutants. No retrospective 2024/2025 values are used.

## Input evidence and decisions
- Charging report 2023, printed p24 Table 4-1: private cars 1029.7 km and 198.0 kWh per month; buses 2889.8 km and 2191.2 kWh. Derived ratios 0.192289016 and 0.758253166 kWh/km. Verified public text transcription, original PDF not retrieved. Coauthor corroborates 2023 report: https://www.ndanev.com/2023/10/20/1-194/. The ratio of group mean charging energy to group mean travel is a sample proxy, not an annual citywide measurement.
- Meter point remains unspecified. The base interprets reported energy as delivered electricity at the end-use boundary. If measured downstream of this boundary, divide only by the corresponding upstream charging efficiency (0.90, 0.92, 0.95 as illustrative stress cases). Peng2017 includes transmission/distribution loss (eq. 5–6 and A8); do not divide by grid efficiency again. Explicitly distinguish charging energy measurement from battery discharge energy.
- Hao et al. (2021), Table 5, Beijing PHEV50 UF 0.66, Beijing PHEV80 0.79, seven-city weighted PHEV50 0.55. CD electricity intensity assumed equal to private BEV proxy; gasoline-mode consumption 7.5 L/100km assumed, CD gasoline set to zero for a simple two-mode proxy (not true for every PHEV).
- Gasoline 7.5 L/100km illustrative existing-fleet proxy; IEA 2021 reports 7.2 Lge/100km for 2019 new LDVs (different scope) and ICCT 2021 documents real-world/type-approval gaps. Test 6 and 9 L/100km. Generic density and LHV conversion from pre-existing ledger =31.8718 MJ/L, not local measured fuel property.
- Lin2015 Table 4 fuel-energy intensities in MJ/km: diesel 13.28/16.77, natural gas 11.72/14.06, diesel hybrid 9.78/13.98 (AC off/on). AC-active share 0.7*4/12 is an old scenario proxy derived from equipped share and four-month operating period; not an observed 2023 fraction. Use source MJ/km directly, avoiding CNG volume/LNG mass mismatch. Mixed residual modelled as diesel hybrid (not observed technology); alternatives all conventional diesel or all gas. Unclassified VKT allocated across conventional fuels by snapshot diesel:gas ratio (explicit proxy). No VKT discarded.
- Peng2017 Table 8 national 2015 gasoline 90.2, diesel 92.3 gCO2e/MJ, grid 203.4 gCO2e/MJ =0.73224 kgCO2e/kWh. Table 10 CNG 72 and LNG pathways 75.9/77.2/78.1 gCO2e/MJ; unknown composition modelled as equal energy shares of CNG and high-LNG endpoint, 75.05, with endpoints tested. Not a measured Beijing mix. The alternative Peng electricity text factor 168 gCO2e/MJ =0.6048 kgCO2e/kWh is separately tested, not averaged. The Table 8/10 electricity boundary is treated as delivered electricity; charging adjustment applied once only if measurement interpretation requires it.

## Equations
Annual gasoline litres = V_ICE*f_ICE/100 + V_PHEV*(1-UF)*f_CS/100.
Private and bus electricity = (V_BEV*e_BEV + V_PHEV*UF*e_CD)/eta (PHEV term private only).
Bus fuel energy = allocated VKT times AC-weighted MJ/km.
WTW tonnes CO2e = gasoline_L*MJ_per_L*EF_g/1e6 + diesel_MJ*EF_d/1e6 + gas_MJ*EF_ng/1e6 + electricity_kWh*EF_grid/1000. S4 halves operational electricity factor only.
Final energy MJ = gasoline_L*MJ_per_L + diesel_MJ + gas_MJ + electricity_kWh*3.6. This is an end-use energy sum, not primary energy.

## Baseline results
| scenario | gasoline million L | electricity GWh | end-use energy PJ | WTW ktCO2e/year |
|---|---:|---:|---:|---:|
| S-1 | 142.189 | 0.000 | 5.099 | 453.331 |
| S0 | 131.673 | 44.743 | 4.619 | 432.689 |
| S1 | 131.673 | 61.121 | 4.417 | 423.293 |
| S2 | 0 | 382.332 | 1.638 | 301.348 |
| S3 | 0 | 398.710 | 1.435 | 291.952 |
| S4 | 0 | 398.710 | 1.435 | 145.976 |

Conditional reduction from S0 to S3 =32.53%, to S4=66.26%. S1 reduces 9.396 ktCO2e/y and S2 131.341 ktCO2e/y under fixed VKT. Combined reduction equals sum of class-specific changes (no interaction under fixed activity and exogenous factors). S4 halving electricity factor halves S3 operating WTW only; it will not halve manufacturing or total vehicle life-cycle burden.

## One-at-a-time sensitivity
15 cases x 6 scenarios = 90 rows. R9_7B_ENERGY_CASES.csv defines each case. S0 range across these cases 356.981–508.396 ktCO2e/y; driven by 6–9 L/100km gasoline assumption. S3 241.140–324.391 ktCO2e/y, driven by alternative grid factor and downstream-meter interpretation. Not a probability/confidence interval and not a jointly optimized worst-case range. AC, gas pathways, residual mixed proxy and UF are retained individually. This does not include R9.7A mileage denominator/transfer uncertainty; future R9.7F must test it separately, not count twice.

## Reproduction
Run python 06_S0_Calculation/r9_7a_activity_scenarios.py then python 06_S0_Calculation/r9_7b_energy_wtw.py. New inputs/results are separate from retrospective R7/R9 files. Independent JS numerical calculation checked 90 rows for nonnegative values, private+bus reconciliation and S3/S4 WTW relationship; Python execution not yet verified. R9.7C will complete manufacturing proxy audit and R9.7D passenger service. R9.7E adds matched manufacturing and local pollutant emissions. No need for manual access to continue; original PDF may be optionally acquired from the public report listing https://m.hibor.com.cn/wap_detail.aspx?id=c5e6812888b46a84efc9187972cdd0f1 if accessible, but its availability does not block calculation.
