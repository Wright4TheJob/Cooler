# Summary
Cooler is a set of python objects that can be used to simulate the transient thermal behavior of a cooler, chiller, or freezer. The original design intent was to compare design trade-offs of an outdoor walk-in freezer, but the components are general purpose enough to simulate a variety of containers.

This approach is intended as a first approximation for a system behavior by only modeling gross heat flow. If your application requires spatial results, such as simulating freezing through a thick cross-section of material, more specialized software will be needed.

# Installation
For a standard installation, navigate in the terminal to the cloned or downloaded repository and run `<python setup.py install>` to perform the local installation

To link the library so that edits to source code propagate, use
`<pip install -e .>` from the repository directory instead.

# Components
## Chiller
This module simulates the performance of a cooling device moving heat from the inside of the container to the outside. Performance of any cooling device depends on design specifications and the relative temperatures of the hot and cold sides of the chiller. Performance curves for refrigeration-cycle heat pumps and thermo-electric elements (TECs) are available. The chiller in a simulation can be initialized using one or two data points from a specifications sheet.

### Assumptions:
* Chiller will not reverse-flow heat back into the cooler. If a negative heat flow is detected, a warning is provided and the heat flow is clamped to zero.
* The chiller can operate at any absolute temperature, and performance is based exclusively on temperature difference between the two sides.

## Contents
This module contains the state of the contents of the cooler and logic for changing state when energy changes. The contents are assumed to be either a liquid or a solid (no boiling is modeled) and store both temperature and liquid fraction to model freezing and thawing behavior.

### Assumptions:
* Contents will not boil.
* Energy is uniformly distributed through contents.
* Contents are uniform in composition (only one material in the cooler).
* Air in the cooler is a negligible thermal mass.

## Insulation
This module calculates rate of heat flow into a cooler for a given difference in temperature between the inside and outside. The effective thermal resistance can be calculated from the geometry of the freezer and properties of insulation used or specified directly if that data is available.

### Assumptions:
* The cooler remains closed and sealed. Heat introduced from air exchange or a door opening should be modeled explicitly in your simulation if required.
* Only one uniform layer of insulation is used. If your cooler uses mixed materials, calculate the effective thermal resistance manually before initializing.

## Weather
If the freezer is a stand-alone structure, outdoor temperature will influence transient system performance. Weather file currently expects columns of an NOAA datetime string and ambient temperature in degrees Celsius. <a href="https://www.ncei.noaa.gov/access/search/data-search/normals-hourly-2006-2020?dataTypes=HLY-TEMP-NORMAL&startDate=2021-12-31T23:00:00&endDate=2021-12-31T23:00:59">NOAA data can be downloaded here for most locations in the USA.</a>

For indoor-located coolers, a constant ambient temperature can be used to simulate performance.

### Assumptions:
* Linear interpolation is used for estimating temperature between provided data points.

# TODO

- [x] Calculation of effective thermal resistance - insulation model
- [x] Contents model. Internal thermal mass + phase change model. Maintain value for internal temperature and calculate new temperature and phase fractions for changes to heat.
- [ ] Multiple contents model - balance energy changes between materials with different thermal properties
- [x] Heat flow model - calculation of instantaneous heat movement based on thermal resistance and temperatures. conductive, maybe convective.
- [x] Heat pump model - coefficient of performance curve. Remove set heat rate by default, maintain temp set point if removing rated heat would drop internal temp below set point.
- [ ] Weather model - typical hourly data for full representative year? Temperature ambient, solar insolation
- [ ] Solar generation simulation - power production based on installation parameters and weather
- [ ] Battery storage simulation - capacity, efficiency, charge state
- [x] Transient simulation - plot power consumption, solar generation, battery charge stare, and  temps for typical day or year. Allow easy modification to system params for quick comparison of alternatives.
- [ ] Costing model - Estimate of price based on insulation, structural, and chiller prices and parametric sizes.
- [ ] Summary report: system up-front price, system energy annual cost, payback period of potential system vs reference design.

# Recommended Transient pure heat transfer calculation loop
0. Initialize temperatures
1. Calculate heat flow over finite time from ambient to interior based on thermal insulation model and respective temps
2. Calculate heat flow over finite time to ambient from interior based on chiller performance and respective temps
3. Apply net heat flow to interior and calculate new interior temps and phases
4. Advance time step

# Recommended Transient full system loop
0. Initialize temperatures
1. Calculate heat flow over finite time from ambient to interior based on thermal insulation model and respective temps
2. Calculate heat flow over finite time to ambient from interior based on chiller performance and respective temps
3. Apply net heat flow to interior and calculate new interior temps and phases
5. Calculate power consumption of chiller
6. Calculate energy generation of solar
7. Apply net energy flow to battery status
8. Advance time step
