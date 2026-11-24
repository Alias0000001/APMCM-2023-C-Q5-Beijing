# R9.7C — Bus and PHEV vehicle-cycle factor audit

## 1. Bus manufacturing proxy — source directly inspected
Lin et al. (2015), Acta Scientiae Circumstantiae 35(2):576–584. Public full text:
https://html.rhhz.net/hjkxxb/html/20140430001.htm
- Figure 2 image was opened and values read directly. Stage GWP values (kg CO2e per 1000 passenger-km): CDB raw materials 2.25, assembly 0.27; NGB 2.50, 0.30; DHEB 2.76, 0.33; BEB 3.06, 0.40.
- Table 5 effective passengers: 42.5, 40.5, 37.5, 34.5; lifetime vehicle distance 400,000 km.
- Derived single-bus manufacturing = (raw-material + assembly intensity) * effective passenger count * 400,000 / 1000. Results: 42.84, 45.36, 46.35, 47.748 t CO2e/bus. Dividing by 400,000 gives 107.10, 113.40, 115.875, 119.37 g CO2e/vehicle-km.
- The same paper explicitly separates vehicle scrapping from material production and assembly; scrap-stage GWP is not included in manufacturing values. It also warns that service-based comparisons differ from vehicle-km comparisons because effective occupancy differs. This supports the conversion, but these are 2011–2014-era historical buses, not 2023 production.
- Important source correction: the earlier R9.6 bus factor table values were arithmetically correct given the figure/table. This audit independently verifies the basis. The hybrid effective passenger count is 37.5, not a guessed value.

## 2. PHEV — no defensible manufacturing-only point estimate recovered
Xiong, Ji & Ma (2019), Energies 12(5), 834, openly accessible:
https://www.mdpi.com/1996-1073/12/5/834
https://res.mdpi.com/energies/energies-12-00834/article_deploy/energies-12-00834.pdf
- Table 2: Qin 80 PHEV-LFP battery 15.2 kWh, lifetime 160,000 km; Qin 100 PHEV-NMC battery 17.1 kWh, lifetime 120,000 km.
- Vehicle-cycle GWP totals reported in the results/Table 8: PHEV-LFP 8,989 kg/vehicle (56.18 g/km x 160,000 km); PHEV-NMC 9,768 kg/vehicle (81.40 g/km x 120,000 km). BEV counterparts: LFP 11,712 kg/vehicle; NMC 13,363 kg/vehicle.
- Crucially, vehicle cycle includes vehicle body, battery, fluids, assembly, transportation, maintenance and end-of-life. It is not manufacturing-only. It must not be labelled manufacturing or directly added to an LCI that already includes those stages. It is retained as a complete vehicle-cycle comparison proxy, useful for a matched BEV/PHEV cross-check.
- Figure 3 provides component shares but not a sufficiently precise machine-readable decomposition for a robust manufacturing-only PHEV factor. Do not estimate an exact manufacturing-only value from pixel percentages.
- Qiao et al. (2017) supplies Chinese ICEV and BEV cradle-to-gate production values: ICEV about 10.0 t and BEV 15.0–15.2 t CO2e. It does not supply a PHEV factor. This confirms the missing PHEV production-only field is not filled by that source.

## 3. Decision for R9.7
1. Use Lin2015 four-type bus raw-material+assembly values as historical manufacturing proxies in a separate bus module. Report range and vintage explicitly; keep EOL separate.
2. For PHEV, do not fabricate a manufacturing-only factor. Use Xiong2019 PHEV vehicle-cycle total only in a separate matched vehicle-cycle sensitivity, or use a clearly bounded battery+body production proxy if a new source provides transparent stage data.
3. Keep current Yang2021 vehicle production and Sun2020 NCM622 battery foreground separate until boundary mapping is reconciled. Do not add a battery manufacturing factor to a BEV/PHEV total that already embeds the battery.
4. R9.7E should allocate annualized embodied burden as annual VKT / lifetime VKT * per-vehicle factor. Bus lifetime 400,000 km is historical; vary it (300k, 400k, 500k). Private passenger-car life should use the source-specific 120k/150k/160k km sensitivity, not a single mixed lifetime.
5. For final matched comparisons, report vehicle-km and passenger-km separately. The bus historical source is passenger-service normalized; convert via its effective occupancy only when explicitly using its assumptions. Do not mix this with measured city PKM as if equivalent.

## 4. Validation status
The bus calculations were independently recomputed and checked. PHEV vehicle-cycle arithmetic is exact from reported g/km and assumed lifetime mileage. A Python script is provided for reproducibility. It is a calculation audit, not proof of 2023 fleet-specific factors.
