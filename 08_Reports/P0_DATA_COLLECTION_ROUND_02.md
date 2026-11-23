# 北京问题五 P0 数据补齐报告（第二轮）

日期：2026-11-23

## 本轮结果

本轮已经找到可以直接进入试算的北京本地数据锚点，并完成两组可复跑的派生估计。

### 1. 私人乘用车 VKT 与动力结构

官方2023年末私人载客汽车保有量为507.3万辆，其中新能源载客汽车52.8万辆。官方资料没有公布52.8万辆内部的BEV/PHEV拆分。

本轮找到的VKT依据：

- 北京2023年私家车日均出行强度：28.4车公里/日。按365天年化，得到全体私人汽车活动量锚点10,366 km/辆·年。
- 北京2023年10月私人纯电乘用车：月均充电9.2次，次均充电行驶169.6 km。派生月VKT为1,560.32 km，年化为18,723.84 km/辆·年。
- PHEV缺少北京2023年度均值，暂采用上海2018年私人PHEV GPS样本年观测窗口均值14,774.95 km作为跨城代理；该数值来自此前表格提取，本轮在线文本提取确认了700辆原始样本、668辆保留样本和2018年全年观测期，但未重新显示该均值，故在最终冻结前仍需复核Table 2原表；Q1、median、Q3暂按此前提取值7,333、12,648、19,373 km做敏感性。
- 旧版比较情景曾采用全国2023年NEV存量中BEV占76.04%的比例（PHEV占23.96%）。经后续核对北京小客车指标政策，该比例不能作为北京中心代理，仅保留为全国结构对照；北京本地BEV/PHEV统计拆分仍未知。

全国结构对照情景（23.96% PHEV share；非北京中心估计）：

| 动力类别 | 北京车辆数估计 | 年均VKT（km/辆） | 年总VKT（亿km） |
|---|---:|---:|---:|
| ICE/非NEV | 4,545,000 | 9,505 | 432.00 |
| BEV | 401,491 | 18,724 | 75.17 |
| PHEV | 126,509 | 14,775 | 18.69 |
| 合计 | 5,073,000 | — | 525.87 |

其中ICE/非NEV年均VKT为残差校准值，使三类车辆总VKT与全体私家车活动量锚点一致；它不是单独观测到的ICE均值。

按100万人代表城市线性缩放：

| 动力类别 | 车辆数 | 年VKT（km） |
|---|---:|---:|
| ICE/非NEV | 207,933 | 1,976,397,649 |
| BEV | 18,368 | 343,922,454 |
| PHEV | 5,788 | 85,513,825 |
| 合计 | 232,089 | 2,405,833,928 |

### 2. 公交动力结构与分动力VKT

2023年公交类别官方总量：
- 运营车辆23,385辆；
- 年总行驶里程11.51亿车公里。

北京公交集团2023年度社会责任报告披露：
- 新能源公交16,832辆；
- 清洁能源与新能源公交占比94.7%。

北京市经济和信息化局2023年6月19日答复披露：公交行业氢燃料电池公交车217辆，均由北京公交集团运营。用它从年末新能源公交总数中扣除时，暂假设6月19日至年末没有新增氢能公交。

以23,385辆作为94.7%清洁能源+新能源占比的同口径分母，才可得到以下暂定结构；该分母匹配尚未在社会责任报告摘要中明确，因此5,314辆和1,239辆均为条件推算，不是官方公布的分动力数量：
- 非氢新能源公交估计16,615辆（暂作BEV/电驱动代理）；
- 氢燃料电池公交217辆；
- 清洁能源公交约5,314辆（CNG/LNG合计，未拆分）；
- 其他公交约1,239辆（未拆分，不能全部标为柴油）。

北京2023年10月电动公交车月均VKT为3,770.8 km/辆，年化45,249.6 km/辆。乘以16,615辆，得到BEV/电驱动公交年VKT估计7.518亿km，约占混合公交总VKT的65.3%。剩余3.992亿km作为未分配的非BEV VKT，不强行拆分到氢、CNG、LNG、柴油、混动或无轨电车。

北京2023年10月电动公交月均电量2,361.3 kWh，百公里电耗62.6 kWh。前者年化为28,335.6 kWh/辆·年；乘以16,615辆非氢新能源公交，得到车队年用电量估计470.8 GWh。该数值仍是单月年化估计，正式排放计算前需确认电量是车辆侧还是购电侧。

### 3. 发现的官方数据通道

北京市统计局公开的2023年部门数据共享制度表 BMZ04-073-108 已明确列出：
- 柴油车、CNG车、LNG车、混合动力车、无轨电车、纯电动车、氢能源车的运营车辆数；
- 汽油、柴油、CNG、LNG、氢能和电力年度消耗量。

公开PDF只是空白报表模板，数值未公开。真正的填报值应通过北京市部门数据共享采集平台或向市交通委申请。它是后续补齐公交动力结构和能源消耗的最直接官方通道。

## 使用结论

- 私人乘用车总VKT：可以形成有依据的基准估计。
- 私人BEV VKT：有北京2023年10月充电大数据支持，年化估计可用于S0并做季节敏感性。
- 私人PHEV VKT：仅跨城代理，需做宽区间敏感性。
- 私人BEV/PHEV车辆数：仅全国存量结构代理，不能称北京实测。
- 公交BEV VKT：可形成带假设的估计。
- 公交非BEV分动力VKT：仍未识别，保留残差，不做虚假拆分。

本轮新增数据及计算脚本均已归档。原始报告PDF因当前归档接口无法取得二进制文件，来源URL、页码/表号及访问状态已登记；没有伪造本地原件。


## 4. Sensitivity and cross-checks

- Private BEV: 2022 monthly charging count × per-charge distance implies 12,384 km/year when annualized; 2023-10 implies 18,723.84 km/year. This is a useful year-on-year sensitivity, but both are annualizations of monthly charging indicators.
- Private PHEV: Shanghai GPS sample Q1/median/mean/Q3 are 7,333/12,648/14,774.95/19,373 km over the annual observation window. Beijing's 2021 seven-city PHEV sample reports 47.1 km/day for Beijing, but its day denominator needs clarification; it is retained as a cross-check, not multiplied by 365.
- Private all-car historical cross-check: Beijing central-city survey means were 12,168 km in 2019 and 10,382 km in 2020.
- Bus: the 2023 MTN prospectus independently reports 2023H1 public-electric-bus VKT of 552 million km; this supports the operator scope of the annual historical series but does not provide propulsion-specific full-year 2023 VKT.
- The official BMZ04-073-108 form contains fuel-specific vehicle counts and energy consumption, but not fuel-specific VKT. A completed form alone will not finish the bus VKT split; a dispatch/odometer extract by propulsion type is still required.

See 02_Cleaned_Data/P0_VKT_intensity_sensitivity.csv for machine-readable values and use restrictions.


## 5. 赛题时点合规说明（重要）

本轮得到的多数“2023年观测值”是在2024年或2025年才公开，因此属于**赛后回顾性重建数据**，不能冒充2023-12-31之前已经公开可得的资料。

- 2023北京统计公报（私人载客汽车507.3万辆、新能源载客汽车52.8万辆）：2024-03-21发布，回顾性数据。
- 北京2023年10月充电行为和电动公交运行数据：2024年报告发布，回顾性数据。
- 北京公交集团2023社会责任报告摘要（16,832辆新能源公交、清洁能源+新能源占比94.7%）：2024-07发布，回顾性数据。
- 全国2023年NEV存量结构（BEV占76.04%）：2024年1月及之后发布，回顾性代理。
- 北京217辆氢燃料电池公交答复：2023-06-19发布，可纳入赛题时点证据，但它是年中快照。
- 北京公交集团2023年中期票据募集说明书：2023-09发布，含2023H1公共电汽车VKT 5.52亿公里，可纳入赛题时点证据，但不是全年数据。
- 北京2021交通发展年报中的2019/2020私人小汽车VKT，以及上海2018 PHEV GPS研究，均在赛题截止日前公开，可用于严格时点代理。

因此，本轮的总VKT活动量锚点适用于**2023年回顾性重建版**；动力结构表中的23.96%仅为全国结构对照情景，不能作为北京中心估计。若论文必须严格遵守2023-12-31资料可得性，不能直接采用2024/2025发布的北京2023年数据，应另建严格时点版：以2019/2020私人车VKT和2023H1公交里程作代理，并将2023年末车辆结构留为未知或情景值。


### 官方公交数据申请入口

2023年BMZ04-073-108表的报送范围是北京市辖区内全部城市公共交通运营企业和出租汽车企业，报送单位为北京市交通委，要求于2024年3月15日前通过北京市部门数据共享采集平台填报。平台地址为：http://43.254.24.235:9999/user/login。表内代码3–9分别是柴油、CNG、LNG、混合动力、无轨电车、纯电动、氢能源车辆数；代码20–25是汽油、柴油、CNG、LNG、氢能源、电力消耗量。公开PDF仅为空表，没有填报值。即使拿到填报表，也仍需另行申请分动力VKT，因为该表没有分动力里程字段。


> **Access-route correction (2026-11-23):** The old `43.254.24.235:9999/user/login` URL is a departmental reporting backend, not a public download portal. Do not ask the researcher to use it. The replacement official channels and the additional round-3 data are documented in [P0_DATA_COLLECTION_ROUND_03_ALTERNATIVE_ACCESS.md](P0_DATA_COLLECTION_ROUND_03_ALTERNATIVE_ACCESS.md).


> **动力结构修订：** 2026-11-23进一步核验发现，北京新能源小客车指标政策定义为纯电驱动，且PHEV可通过普通指标登记。原全国76.04% BEV比例已降级为对照情景。请以 `03_Data_Audit/P0_EVIDENCE_AUDIT.md` H节及 `08_Reports/P0_DATA_COLLECTION_ROUND_04_PRIVATE_NEV_POLICY_AUDIT.md` 为准。
