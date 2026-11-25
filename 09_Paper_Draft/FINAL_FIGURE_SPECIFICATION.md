# Final figure specification (new assets only)

All figures in English; white background; vector SVG and PDF export where available; use embedded or reliably available fonts, 8–10 pt minimum at intended printed size; no overlapping labels, no decorations, no gradient. Consistent mode colors: private #496783, bus #D3A16F; stage fill production #82ADD0 and WTW #496783 (when stage is color, use mode facets rather than encode mode with competing palette). Use scenario labels S−1, S0…S4. Axis includes unit; direct labels only when legible. Each figure caption states source table, period, annual million-city scope, modeled boundary and assumptions. No plot of missing stages as zero. Each panel has its own unit; use a zero baseline for bars and a clearly labelled zero-reduction reference line for sensitivity ranges.

| Figure | Purpose and design | Data |
|---|---|---|
| 1 | Left-to-right framework: reference-city evidence → target-city activity and propulsion → energy/climate/local-emission tracks → six scenarios → sensitivity; no internal version labels | manuscript equations |
| 2 | Two-panel baseline VKT allocation: private ICEV/BEV/PHEV and bus diesel/gas/mixed/BEV/unclassified; label million vehicle-km/year and shares | R9.7A six-scenario VKT |
| 3 | Environmental boundary matrix: vehicle production and WTW included; generic non-exhaust wear screening shown separately; maintenance/EOL/infrastructure, resuspended dust and secondary PM remain unquantified; battery-only LCIA separate | R9.7C, Audit-04 |
| 4 | Energy-carrier structure by scenario, with gasoline, diesel, natural gas and electricity separated; total final energy in PJ/year | R9.7B energy cases |
| 5 | Two mode facets, stacked production and WTW GWP bars (kt CO₂e/year), all six scenarios; label partial life-cycle boundary | R9.7B/C |
| 6 | Five small multiples of mode-stacked combustion-exhaust bars (t/year), independent y axes; zero bars refer only to modeled combustion exhaust | R9.7E road pollutant rows V_reference |
| 7 | Mode-specific g CO₂e/VKT and conditional g CO₂e/PKM comparison; state occupancy and trip-distance proxies | R9.7D |
| 8 | Transfer grid heatmap (g×m, panels b) for S3 paired reduction; common color scale and matched S0 baseline | R9.7F transfer grid |
| 9 | Horizontal paired reduction ranges with point reference values and zero line, signed percent, 14,580 climate sets | R9.7F nested envelope |
| 10 | Private-car BEV break-even electricity WTW factor across lifetime mileage; label the vehicle pair and partial-GWP boundary | R9.7B/C |


Acceptance: independently validate data totals, check SVG XML, render to PDF/PNG and visually inspect at print width; ensure symbols/subscripts and legend readable; verify no panel clipping or text collision; confirm manuscript cross references, all original assets preserved. Figures 1–10 are referenced by the current English manuscript and must all pass final rendering and print-width inspection. Figure 11 remains a supplementary charging-boundary asset and is not currently referenced in the manuscript. Do not claim visual approval until actual rendering and inspection.

## G-2 implementation
11 contest figures and 9 retrospective diagnostic figures generated as separate SVG/PNG pairs from repository CSVs. Final manuscript figures numbered in reading order; filenames are stable identifiers. Historical figure numbers are encoded in Legacy_* filenames and mapped in FIGURE_DIAGNOSTIC_APPENDIX.md. User's palette, non-energy split, chemistry difference panels, threshold band and coverage/LCIA safeguards are implemented. CI renders and verifies files and links; visual inspection remains a separate gate.
