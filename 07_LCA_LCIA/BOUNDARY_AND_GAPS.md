# LCA / LCIA boundary and input status

## Model boundary to preserve

The project framework distinguishes:
1. Vehicle manufacturing.
2. Traction-battery manufacturing and replacement.
3. Energy supply: fuel well-to-tank (WTT) and electricity generation/transmission/charging.
4. Vehicle operation: fuel combustion or electricity use.
5. Maintenance and component replacement.
6. End-of-life treatment and recycling.

The annualized life-cycle burden is not the same as the emissions physically released during a calendar year. The calculation must state its vehicle lifetime, lifetime VKT, replacement assumptions, recycling allocation, and whether manufacturing factors already include the traction battery.

## Local road emissions versus full life cycle

Local road emissions cover the relevant road-operation emissions and must not be added a second time on top of a full life-cycle inventory that already includes the same operation stage. Upstream power generation and vehicle/battery manufacturing may occur outside Beijing and must not be described as local roadside emissions.

## Electricity

The available 2023 Beijing provincial average electricity CO2 factor is 0.5554 kg CO2/kWh, published 2025-12-31. It is an operational CO2 factor. It is not, by itself, a cradle-to-grave electricity CO2e factor. Charging losses and the distinction between battery-side and grid-side consumption must be handled exactly once.

## Inputs not yet admitted

- Private ICE fuel consumption (L/100 km) for the chosen vehicle class and duty cycle.
- Private BEV electricity consumption (kWh/km), with battery-side versus grid-side definition.
- Private PHEV fuel/electricity use and a fleet-weighted utility factor.
- Public bus energy use and propulsion-specific VKT.
- Vehicle body and powertrain manufacturing factors, with battery inclusion/exclusion stated.
- Battery chemistry, capacity, manufacturing factor, life, and replacement count.
- Maintenance and end-of-life factors.
- Non-exhaust PM factors matched to vehicle mass, tyres, brakes, and road conditions.
- LCIA characterization method/version and flow-to-factor mapping.

## Double-counting controls

1. Do not add battery manufacturing twice if an EV vehicle-manufacturing factor already includes the battery.
2. Do not add WTT twice if a fuel WTW factor is used.
3. Do not apply charging losses twice.
4. Do not add local road emissions again after they have already been counted in the life-cycle operation stage.
5. Do not mix CO2 and CO2e factors or apply GWP conversion twice.
6. Do not combine a bus fleet's passenger trips with a passenger-km denominator without average trip distance or direct turnover data.
