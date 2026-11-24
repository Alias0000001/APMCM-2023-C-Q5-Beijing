# Environmental Impacts of Vehicle Electrification in a City of One Million Residents

## Problem 5 — contest-facing manuscript working structure

This document is a structural revision, not a submission-ready paper. The final abstract and numeric tables must be populated by the competition-time scenario pipeline. The previous R9.5 manuscript remains an internal retrospective record.

## 1. Problem restatement

We assess the environmental consequences of electrifying private passenger cars and public buses in a representative city of one million residents. Our objective is to quantify the annual environmental burdens associated with alternative propulsion technologies, distinguish local road emissions from upstream and manufacturing impacts, and identify conditions under which electrification yields environmental benefits.

## 2. Representative-city construction

The target population is fixed at one million. A real city's publicly documented transport statistics provide empirical reference rates for vehicle ownership, vehicle use and bus supply; the reference city itself is not the object of inference. Beijing is considered as a data anchor because its vehicle and bus activity evidence can be paired with Chinese technology studies. Its metropolitan scale and transport structure differ from those of a typical million-resident city. We therefore transfer per-capita activity parameters, subject to explicit spatial and mobility adjustments, rather than assuming that an arbitrary part of Beijing is the target city. All estimates use information available before the competition deadline.

Let P*=1,000,000. Define n as private cars per resident, d as annual vehicle-kilometres per car and b as annual urban bus vehicle-kilometres per resident. Let c_n, c_d and c_b be transfer corrections for ownership, urban travel and bus supply, respectively. Then V_P=P* n d c_n c_d and V_B=P* b c_b. The baseline uses the documented reference rates; transfer sensitivity examines the influence of plausible differences. If the source mileage includes travel outside the defined reference boundary, apply a separate spatial fraction only once. Avoid overlapping it with c_d.

## 3. Model framework and assumptions

We develop a transport-activity model, a propulsion-scenario allocation model and a common-boundary environmental accounting model. The activity model determines annual travel by private cars and buses; the scenario model redistributes this travel among technologies while holding class-specific travel demand fixed. The accounting model multiplies annual vehicle-kilometres by matched environmental intensities. Manufacturing and other embodied burdens are allocated over vehicle lifetime mileage. Local road emissions are calculated separately from the annualized life-cycle or matched-stage burdens.

Vehicle-kilometres are the primary functional unit for propulsion substitution; passenger-kilometres provide a supplementary equal-service comparison using distance-weighted occupancy scenarios. Bus and car comparisons in passenger-kilometres are not inferred from vehicle-kilometres alone.


### 3.1 Manufacturing-burden annualization

The manufacturing burden is annualized under a steady-state replacement assumption. For vehicle technology (k), let (M_k) denote the production-stage GWP per vehicle and (L_k) its lifetime mileage. The annualized burden is
[
G_{k,s}^{\mathrm{prod}}=\frac{VKT_{k,s}}{L_k}M_k.
]
For private cars, the provisional GWP factor set uses Qiao et al. (2017) for ICEV and BEV-NMC and Xiong et al. (2019) for PHEV-NMC; all factors include the initial traction battery. For buses, Lin et al. (2015) provides historical raw-material and assembly GWP factors for diesel, natural-gas, diesel-hybrid and battery-electric buses. These factors are annualized over 150,000 km for passenger cars and 400,000 km for buses. An independent matched CO2-only set from Yang et al. (2021) is retained as a cross-check, not added to the GWP ledger.

The production GWP factors are added to the well-to-wheel operating GWP only after the impact metric and unit are harmonized. The resulting comparison is a partial LCA because maintenance, end-of-life, infrastructure and non-exhaust emissions are not yet included. The 2018 Hangzhou bus study is used as a separate manufacturing-boundary sensitivity; its CO2-only results are not averaged with the Beijing GWP factors.

## 4. Electrification scenarios

| Scenario | Private cars | Buses | Charging electricity |
|---|---|---|---|
| S−1 | All conventional combustion | All conventional combustion | Baseline |
| S0 | Estimated prevailing mix | Estimated prevailing mix | Baseline |
| S1 | S0 mix | All BEV | Baseline |
| S2 | All BEV | S0 mix | Baseline |
| S3 | All BEV | All BEV | Baseline |
| S4 | All BEV | All BEV | Lower-carbon supply |

Maintain gasoline, natural gas, diesel and PHEV distinctions where used in the baseline. A PHEV has both fuel and electric travel. Define the conventional bus reference mix and account for every vehicle-kilometre.

For vehicle class i, technology k, scenario s, and a matched environmental indicator h:
V(i,k,s)=V(i,s) p(i,k,s), with sum_k p(i,k,s)=1.
B(s,h)=sum_(i,k) V(i,k,s) [M(i,k,h)/L(i,k)+U(i,k,s,h)].
M denotes the total embodied burden of the included stages per vehicle; U denotes the matched per-kilometre operating burden. Manufacturing and energy boundaries are stated alongside the results; a two-stage result is named accordingly. For local road emissions use tailpipe and supported non-exhaust intensities separately, not upstream factors. Green electricity modifies U only. GWP and individual pollutant masses are reported independently.

The remaining sections are to be populated from verified contest-time results: data and factors; baseline activity and energy; six-scenario results and reductions; local pollutant trade-offs; sensitivity to transfer, energy, occupancy and lifetime; break-even conditions; validation; concise strengths and limitations; conclusion. No R-series release labels or retrospective verification will appear in the final submission.
