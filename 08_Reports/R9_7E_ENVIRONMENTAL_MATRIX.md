# R9.7E — Six-scenario road exhaust and environmental matrix

## Source and scope
China Society for Environmental Sciences, Technical guideline on city-level air pollutant emission inventory development, August 2023 consultation draft, Appendix F: gasoline small/micro passenger cars F.1 printed p55; diesel buses F.2 p57; natural gas buses F.3 p59. Original table screenshots checked. Draft https://cmsfiles.zhongkefu.com.cn/cmshuanjingapp/upload/resource/W020230822432828039219.pdf; accompanying August 2023 explanation https://cmsfiles.zhongkefu.com.cn/cmshuanjingapp/upload/resource/W020230822432829025889.pdf. The 2024 final standard is not used. These are national composite basic emission factors (g/vehicle-km), not measured 2022/2023 Beijing fleet means, and no speed/temperature/age corrections or actual fleet standard weights are available. China V is an illustrative reference; IV and VI homogeneous standard stresses are not fleet estimates or confidence bounds. The Beijing 2019 new-registration standard notice https://www.beijing.gov.cn/zhengce/gfxwj/201912/t20191219_1311796.html motivates including VI, but does not establish existing fleet composition. VOCs retains the source indicator; evaporative coverage is not established, do not claim a complete VOC inventory. PM2.5 and PM10 overlap; never sum them.

## Equations
E_p = sum VKT_k * EF_k,p / 1e6 (tonnes/year). PHEV charge-sustaining fraction 1-UF times gasoline proxy; ignores CD engine starts and cold-start difference. Hybrid residual uses diesel bus factor as reference, not fuel-saving proportionality; 0.75 multiplier is exploratory only. Separate alternative assignments of mixed residual to diesel or gas. Unclassified bus allocation follows R9.7B diesel:gas count ratio. BEV zero combustion exhaust only. Non-exhaust tyre/brake/road wear, road dust, evaporative emissions not separately quantified; upstream electricity/fuel pollution and full vehicle-cycle pollutants not in this matrix. No air concentration/health calculation. Eight cases x six scenarios x five pollutants = 240 rows. Matrix retains R9.7B and C climate results with their unchanged boundaries; no addition of pollutant masses to GWP or WTW CO2e to road pollutant mass. Sensitivity cases apply only to exhaust; energy/GWP matrix uses base inputs.

## Reference results
Units PJ, ktCO2e/year, and pollutant tonnes/year.
|Scenario|Energy|WTW GWP|Production GWP|Partial GWP|CO|VOCs|NOx|PM2.5|PM10|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|S-1|5.099|453.331|131.258|584.589|1087.752|230.944|728.715|7.645|7.857|
|S0|4.619|432.689|135.100|567.789|968.961|212.230|364.259|6.830|7.004|
|S1|4.417|423.293|135.232|558.525|930.486|210.676|105.338|5.267|5.267|
|S2|1.638|301.348|194.894|496.242|38.475|1.554|258.921|1.563|1.737|
|S3|1.435|291.952|195.026|486.978|0.000|0.000|0.000|0.000|0.000|
|S4|1.435|145.976|195.026|341.002|0.000|0.000|0.000|0.000|0.000|
S3 and S4 exhaust is structurally zero only for covered direct combustion flows, not zero road PM or total pollution. S4 changes electricity GWP only, so road exhaust equals S3. All life-cycle climate values remain partial: manufacturing+WTW; maintenance/EOL/infrastructure missing, no zero filling. The table is a 100万人 hypothetical representative city using Beijing reference rates, not measured Beijing emissions.

## Reproduction
Run python 06_S0_Calculation/r9_7e_environment.py after A/B/C. Independent JS arithmetic verified nonnegative outputs and reconciliation. Next R9.7F: layered transfer and uncertainty using R7.1/R8; do not re-search unavailable Jinhua VKT.
