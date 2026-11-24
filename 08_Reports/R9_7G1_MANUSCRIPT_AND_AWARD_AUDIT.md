# R9.7G-1 — Manuscript reconstruction and award-paper benchmark

Rechecked team apmcm2303763 Section VIII pp.19–21 in the published compilation (https://newoaa.shisu.edu.cn/_upload/article/files/36/c4/7e46748e4857afe7f28b38b53757/fdc80a98-af27-4bd0-9f04-209196231db4.pdf). The text and equation (9) were available; the PDF screenshot request failed because the compilation was too large. Figure layout is therefore based on prior repository style audit, not a new visual inspection of that compilation. The paper fits ownership/population and reports 1,161 buses, 1,046,500 vehicles and 21,545,123.478 kg CO2 per common 100-km exposure. Its energy-equivalence-to-gasoline method is not a physical grid WTW calculation.

| Comparison | Award paper | Current manuscript |
|---|---|---|
| Target | 1 million | 1 million |
| Vehicle scope | fitted total vehicles minus buses; trucks excluded by assumption | private small/micro passenger cars plus operator buses |
| Activity | same 100 km per vehicle | annual mode VKT, propulsion allocation; conditional PKM |
| Energy | fuel-equivalent | carrier-specific demand and WTW |
| Outcomes | CO2 estimate | included-stage CO2e, energy, separate road exhaust |
| Verification | fitted population relationship | conservation, stage reconciliation and paired stress |

Common-distance diagnostic (not matched GWP validation): award implied 205.88 g CO2/km. For our S0, use 225,793.16 private cars and 1087.17 operator buses per million (April 2023 snapshot transferred to 2022 population, not annual fleet observation), and apply each mode's S0 VKT-weighted WTW factor to 100 km per vehicle. This gives 4826492 kg CO2e and 212.73 g CO2e/km. Different scopes, propulsion weighting, time and impact units make numerical agreement or model-error percentage invalid; this normalization only removes distance-exposure differences. Never tune to award-paper output. The award paper and 2024 COMAP examples are post-contest methodological references, not model inputs or citations inside the contest-facing paper. COMAP current instructions (https://contest.comap.com/undergraduate/contests/mcm/instructions.php) are a writing reference, not an APMCM submission-rule assertion.

The new manuscript is Q5_Contest_Manuscript_EN.md. Old drafts untouched. All result tables assembled from R9.7 A–F CSVs; abstract updated, both modes shown, internal version names excluded from body, later Jinhua numbers isolated from contest manuscript. Explicitly not final typeset paper. References retain repository source URLs; author/title bibliographic verification and final figure render review remain pending. The user-provided task book ends mid-list; no additional unseen requirements presumed.
