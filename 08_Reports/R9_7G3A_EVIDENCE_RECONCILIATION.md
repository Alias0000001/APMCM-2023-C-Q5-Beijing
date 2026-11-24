# R9.7G-3A — Reconcile earlier evidence and quantify bus scrapping sensitivity

As of 2026-11-24, work/paper-model-audit-20261124 parent 4a914b3. The user supplied the earlier R9.6 evidence report. This note reconciles it rather than restarting the searches. Main and the earlier work branch are untouched.

## Charging evidence
Re-read 2023 report Table 4-1 (printed p24), transcribed copy https://www.scribd.com/document/1005901118/2023%E5%B9%B4%E4%B8%AD%E5%9B%BD%E4%B8%BB%E8%A6%81%E5%9F%8E%E5%B8%82%E5%85%85%E7%94%B5%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E7%9B%91%E6%B5%8B%E6%8A%A5%E5%91%8A-%E4%B8%AD%E8%A7%84%E9%99%A2 : private car 1029.7 km and 198.0 kWh; bus 2889.8 km and 2191.2 kWh. Contemporary September 2023 release coverage https://finance.sina.com.cn/tech/roll/2023-09-05/doc-imzkquit8803966.shtml. Original 2023 PDF still not archived; the transcribed table and contemporaneous release are evidence, not an official PDF archive. Independently visually checked the 2024 report printed p25 (PDF page 29) https://file.jgvogel.cn/125/upload/resources/file/574928.pdf: 2022 fields match all four values; 2023 private 1551.6 km / 248.7 kWh, bus 3770.8 km / 2361.3 kWh. The 2023 row is retrospective only; 15.2 kWh/100 km is taxi not private. Keep contest car 198/1029.7 and bus 2191.2/2889.8; retain older R7 corrected 0.160 and 0.626 in retrospective ledger. No meter location established, no double charging-loss adjustment.

## Bus service
Official historical operator table https://www.bjbus.com/home/fun_statistics.php now gives 2022 983.69 million km and 1.72558 billion boardings, consistent with contemporaneous rounded 984 million and 1.726 billion used in the contest baseline. 2023 public bus/trolleybus column 1.151 billion km and 2.08687 billion boardings; ratio 1.813093 boardings/vehicle-km, not occupancy. Group total is a different scope. Current table is retrospective; 2023 full-year data cannot enter contest-time baseline. Actual matched PKM remains NA; prior conditional service calculation stands. Lin2015 Table5 provides modeled occupancy based on 0.45 load and a 400,000-km life, not observed 2023 occupancy.

## Manufacturing and newly quantified scrapping
Directly inspected original Figure 2 https://html.rhhz.net/hjkxxb/html/PIC/20140430001-2.jpg and Table 5 https://html.rhhz.net/hjkxxb/html/20140430001.htm. Materials and assembly values match the existing manufacturing ledger. Correct unit conversion: for a kg CO2e/1000 PKM source factor f, effective passengers o, lifetime km L, tonnes/vehicle = f*o*L/1e6; dividing by 1000 yields kg, not tonnes. The prior table values and executable manufacturing factors are already correct; the earlier prose formula was ambiguous/wrong for tonnes. The 2024 Harbin study remains excluded, and its reported internal discrepancy is not resolved here.

Figure 2 also explicitly reports vehicle scrapping 0.04/0.04/0.06/0.17 kg CO2e per 1000 PKM for diesel/gas/hybrid/BEV. Converted to 1.700/1.620/2.250/5.865 g CO2e/VKT. These are historical source-defined scrapping loads, not a comprehensive end-of-life inventory, and no independent recycling credit is added. Use the same bus technology allocation as R9.7C to compute a separate expansion only; keep A–F baseline frozen and other missing stages NA.

|Scenario|Bus scrapping (t CO2e/y)|Expanded partial GWP (kt/y)|Reduction vs paired S0 (%)|
|---|---:|---:|---:|
|S-1|73.629|584.662|-2.940|
|S0|176.439|567.965|0.000|
|S1|264.211|558.789|1.616|
|S2|176.439|496.418|12.597|
|S3|264.211|487.242|14.213|
|S4|264.211|341.266|39.914|
Reproduce: python 06_S0_Calculation/r9_7g3_bus_scrapping.py. The supplementary calculation is not a complete LCA and does not replace the main result matrix.

## Figure review and test state
G-2 CI run 45408698927 succeeded; 40 actual assets at 4a914b3. Using base64 file retrieval, visually inspected Legacy_03, 05, 06 and 07 PNGs. Dual-scale stage plot and separate chemistry-difference panels are present; lower bus row in Legacy_03 is crowded at axis edge, and the very narrow Legacy_07 band is mostly obscured by its midpoint line at full plot scale. Further print-layout work: pad rows and add an explicitly scaled chemistry-difference panel or table for threshold band. Remaining 16 figures and typeset manuscript still require visual review; not declared final.
