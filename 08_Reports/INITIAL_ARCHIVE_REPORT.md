# Initial archive report — Beijing Problem 5

Date: 2026-11-23

## What has been archived

- Project README and data-governance rules.
- Project scope and change log.
- Raw-source availability manifest.
- Structured Beijing 2023 official observations.
- Source register with geographic and methodological caveats.
- Parameter register with baseline eligibility flags.
- First-pass population-scaled table for a 1,000,000-person representative city.
- Reproducible Python scaling script.
- Beijing data audit and LCA/LCIA boundary-gap notes.

## First-pass scaling result

The population scaling factor is:

0.045749839876 = 1,000,000 / 21,858,000.

The official 2023 private passenger vehicle count of 5.073 million scales to approximately 232,089 vehicles. The 528,000 new-energy private passenger vehicles scale to approximately 24,156 vehicles, but the result remains an aggregate NEV count with no BEV/PHEV split.

The public bus category count and operator activity totals have also been scaled for a first-pass comparison. These are derived estimates, not local observations, and the operator scope and source label are retained. No bus propulsion split or PKM is inferred.

## What has not been archived

- Original Zenodo CSV bytes (only the prior audit metadata and script are available in this workspace).
- Original Beijing transport annual report PDF used for the 2019/2020 private-car mileage cross-check.
- Full source PDFs for the PHEV utility-factor study and Shanghai PHEV GPS study.
- Vehicle-specific energy-use data and LCA/LCIA factor files.

## What cannot yet be calculated defensibly

- Beijing 2023 private passenger VKT by ICE/BEV/PHEV.
- BEV/PHEV shares within the 528,000 new-energy private passenger vehicles.
- Public bus BEV/ICE activity split.
- Bus PKM.
- Private-car urban VKT share alpha_P.
- Complete operational emissions and full life-cycle impact totals.

## Release status

This is an initial auditable repository, not a final model result. The missing inputs remain blank or explicitly quarantined. The next data round should prioritize original source-file archiving, private passenger VKT, propulsion cross-tabs, and bus propulsion-specific activity.
