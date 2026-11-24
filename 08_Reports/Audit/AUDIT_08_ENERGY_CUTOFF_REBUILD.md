# Audit-08: contest-time energy input reconstruction

Date: 2026-11-25  
Working branch: \`work/paper-audit08-contest-time-20261125\`  
Parent reference commit: \`d390dc4a9b67c44fa020ac39d6e25f705c46e4f0\`  
Scope: correct the R9.7B energy parameters before writing the contest manuscript. The original post-cutoff input and outputs remain preserved on the parent branch.

## 1. Why the previous energy baseline is not admissible

The former R9.7B energy parameters were derived from the 2024 China Major Cities Charging Infrastructure Monitoring Report (Table 4-1). Although part of the underlying observations refer to October 2022, the report was published in 2024, after the APMCM 2023 submission deadline (2023-11-27 09:00 Beijing time). The audit standard distinguishes observation year from publication date. These values are therefore retained only for retrospective comparison and are excluded from the contest-time main model.

The former private-car value also had a reconciliation defect: \(198/1029.7=0.192289\) kWh/km, or 19.23 kWh/100 km, while the source register separately recorded 16.0 kWh/100 km for the private passenger-car row. A ratio of group means must not be silently treated as the same statistic as a reported group intensity.

## 2. Pre-cutoff replacement for private BEVs

Use Jin, Wang and He (ICCT, April 2023), based on 2021 operating data for ten popular private BEV models in five Chinese cities. The report gives MIIT nominal energy intensity by model, Beijing sample counts (44,047 vehicles in total), and Beijing-specific real-world range differences under all driving conditions.

For models with a Beijing Figure 6 value, reconstruct the model-level real-world energy median by
\[
e_j^{RW}=\frac{e_j^{nom}}{1+\Delta r_j},
\]
where \(\Delta r_j\) is the digitized fractional difference between Beijing real-world range and nominal range. This follows the report's Appendix B range definition. The model-level medians are weighted by the Beijing sample counts:
\[
e_{car}=\frac{\sum_j n_j e_j^{RW}}{\sum_j n_j}.
\]

Car 8 has no Beijing point in Figure 6. It accounts for only 87 of 44,047 Beijing samples (0.20%); its value uses the report's Figure 4 all-city, all-condition median energy increase of approximately 20%. This exception is explicitly recorded in \`R9_7B_PRIVATE_BEV_ENERGY_RECONSTRUCTION.csv\`.

Result: \(e_{car}=0.1583904627\) kWh/km. The Beijing-sample-weighted nominal benchmark is 0.1321126524 kWh/km. A cold-condition upper stress uses 1.60 times the nominal benchmark, anchored to the report's 25%–60% increase in Beijing cold conditions. These are weighted medians from selected models, not a raw citywide fleet mean.

## 3. Pre-cutoff replacement for electric buses

Use Ma et al. (Energy 210, 2021, 119196), a Beijing bus-network study covering 630 routes. The reported electric-bus energy consumption is 14.1 L/100 km on an energy-equivalent basis. Convert explicitly:
\[
e_{bus}=\frac{14.1\;L/100km\times36\;MJ/L}{3.6\;MJ/kWh\times100\;km}=1.41\;kWh/km.
\]

This is a historical Beijing route-based energy proxy, not a 2023 fleet-wide charging-meter observation. A ±20% design stress (1.128–1.692 kWh/km) is used as an uncertainty range, not a confidence interval. The ICCT 2023 selected city-bus model value of 0.527 kWh/km is retained as a separate alternative technology proxy, not as the Beijing fleet mean.

## 4. Charging boundary

The new private-car and bus energy values are vehicle-side energy proxies. To convert them to grid input, the main calculation uses \(\eta=0.92\), transferred from the World Bank Shenzhen Bus Group case study (p.108). This is a design/transfer assumption, not a Beijing observation. The sensitivity set includes \(\eta=0.90\), 0.95 and 1.00. The paper must state that the local meter point remains unknown.

## 5. Reproducibility and paper-use rules

- \`R9_7B_PRIVATE_BEV_ENERGY_RECONSTRUCTION.csv\` preserves the ten-model inputs and weighted reconstruction.
- \`R9_7B_BUS_ENERGY_DERIVATION.csv\` preserves the energy-equivalent conversion.
- \`R9_7B_ENERGY_INPUTS.csv\` retains old monthly fields with \`POST_CUTOFF_RETROSPECTIVE_ONLY\` status; they are not used by the main model.
- \`r9_7b_energy_wtw.py\` independently verifies both reconstructed energy inputs before calculating WTW energy.
- The six-scenario outputs, source sensitivity, PKM diagnostics, Jinhua retrospective diagnostic, and final remediation figures must be regenerated from the new input.
- No 2024/2025 observation or report may be described as information available to a 2023 contest team.

This correction changes the numerical baseline. The prior six-scenario results remain preserved in the parent branch and must not be mixed with the regenerated contest-time outputs.
