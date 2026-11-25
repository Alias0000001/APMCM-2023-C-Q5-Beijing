# R9.7G-1 — Manuscript reconstruction and same-contest exemplar benchmark

Rechecked the officially compiled 2023 APMCM C5 exemplar, team apmcm2303763, Section VIII pp.19–21 in the APMCM entry-manual compilation (https://newoaa.shisu.edu.cn/_upload/article/files/36/c4/7e46748e4857afe7f28b38b53757/fdc80a98-af27-4bd0-9f04-209196231db4.pdf). The text and equation (9) were available; the PDF screenshot request failed because the compilation was too large. Figure layout is therefore based on prior repository style audit, not a new visual inspection of that compilation. The sample is included in the organizing committee's 'excellent papers' section. Its exact prize grade was not confirmed in the official award-list search, so this audit does not label it First Prize or Grand Prize. The paper fits ownership/population and reports 1,161 buses, 1,046,500 vehicles and 21,545,123.478 kg CO2 per common 100-km exposure. Its energy-equivalence-to-gasoline method is not a physical grid WTW calculation.

| Comparison | Award paper | Current manuscript |
|---|---|---|
| Target | 1 million | 1 million |
| Vehicle scope | fitted total vehicles minus buses; trucks excluded by assumption | private small/micro passenger cars plus operator buses |
| Activity | same 100 km per vehicle | annual mode VKT, propulsion allocation; conditional PKM |
| Energy | fuel-equivalent | carrier-specific demand and WTW |
| Outcomes | CO2 estimate | included-stage CO2e, energy, separate road exhaust |
| Verification | fitted population relationship | conservation, stage reconciliation and paired stress |

Common-distance diagnostic (not matched GWP validation): award implied 205.88 g CO2/km. For our S0, use 225,793.16 private cars and 1087.17 operator buses per million (April 2023 snapshot transferred to 2022 population, not annual fleet observation), and apply each mode's S0 VKT-weighted WTW factor to 100 km per vehicle. This gives 4826492 kg CO2e and 212.73 g CO2e/km. Different scopes, propulsion weighting, time and impact units make numerical agreement or model-error percentage invalid; this normalization only removes distance-exposure differences. Never tune to award-paper output. The officially compiled same-contest exemplar is used only as a writing benchmark, not as model input or a source for our technical parameters. Its method is deliberately not copied because its gasoline-equivalent electricity treatment and simplified vehicle scope do not match our WTW/LCA boundary. 2024 COMAP examples remain secondary writing references, not model inputs or citations inside the contest-facing paper. COMAP current instructions (https://contest.comap.com/undergraduate/contests/mcm/instructions.php) are a writing reference, not an APMCM submission-rule assertion.

The new contest-facing manuscript is Q5_Contest_Manuscript_EN.md. Old drafts are preserved. The English paper has been rewritten to follow the same-contest sample's Summary Sheet → Contents → assumptions/notations → problem analysis → nested model → results → sensitivity/error analysis → model evaluation sequence. It includes a six-scenario core-results table, explicit baseline activity and propulsion VKT, carrier-specific energy/WTW, annualized vehicle production, local exhaust and non-exhaust PM screening, conditional PKM, and a Jinhua transferability boundary check. Jinhua's 2022 statistical yearbook was published in October 2023, before the contest deadline; only its pre-contest city-district population and road-passenger boundary indicators are used. No matched Jinhua VKT/PKM or absolute Jinhua emissions total is fabricated, and post-cutoff retrospective Jinhua diagnostics remain excluded. The manuscript is not final typeset. Bibliographic cross-check, page count and final figure render review remain pending.


## Writing benchmark revision (2026-11-25)

A direct same-contest C5 sample has now been identified in the APMCM organizing committee's compiled entry manual: Team apmcm2303763, Question 5, pp.19–21. Its chapter uses a clear data-description → nested population/vehicle-count fit → emissions model → immediate numerical result → sensitivity/error analysis → model evaluation sequence. It uses Figure 13 for population/vehicle-count evidence and Figure 14 for the emissions fit. The team is listed in the manual's "excellent papers" compilation; exact award grade was not confirmed in the published award-list search.

The contest-facing English manuscript will be rewritten around this structure, but will not copy the exemplar's simplifying assumptions or fuel-equivalent electricity method. The project has a direct same-contest style analysis at 09_Paper_Draft/2023_APMCM_C5_优秀论文写作拆解.md.


## Manuscript rewrite completed (2026-11-25)

The same-contest exemplar has been analyzed in 09_Paper_Draft/2023_APMCM_C5_优秀论文写作拆解.md. The English manuscript now contains a first-page Summary Sheet and hierarchical Contents; explicit assumptions and notation; problem analysis; a two-stage population-to-activity and activity-to-environment model; all six scenarios; a core six-scenario results table at the start of the results chapter; separate exhaust and non-exhaust PM tables; Jinhua's pre-contest external boundary check; propulsion-share and mileage-denominator sensitivities; 14,580 paired stress cases; equal-PKM sensitivity; break-even grid factor; verification and limitations.

A formula/unit review corrected WTW fuel factors to kg/MJ before tonne conversion and retained production factors in tonnes/vehicle. All ten figures referenced by the current manuscript exist in the repository. Visual typesetting and final page-limit review are still pending. No input CSV, baseline calculation or main branch was modified by the writing pass.
