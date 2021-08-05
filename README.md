# Freezer Design Modules

[x] Calculation of effective thermal resistance - insulation model
[x] Contents model. Internal thermal mass + phase change model. Maintain value for internal temperature and calculate new temperature and phase fractions for changes to heat.
[ ] Multiple contents model - balance energy changes between materials with different thermal properties
[x] Heat flow model - calculation of instantaneous heat movement based on thermal resistance and temperatures. conductive, maybe convective.
[x] Heat pump model - coefficient of performance curve. Remove set heat rate by default, maintain temp set point if removing rated heat would drop internal temp below set point.
[ ] Weather model - typical hourly data for full representative year? Temperature ambient, solar insolation
[ ] Solar generation simulation - power production based on installation parameters and weather
[ ] Battery storage simulation - capacity, efficiency, charge state
[x] Transient simulation - plot power consumption, solar generation, battery charge stare, and  temps for typical day or year. Allow easy modification to system params for quick comparison of alternatives.
[ ] Costing model - Estimate of price based on insulation, structural, and chiller prices and parametric sizes.
[ ] Summary report: system up-front price, system energy annual cost, payback period of potential system vs reference design.

# Transient pure heat transfer calculation loop
0. Initialize temperatures
1. Calculate heat flow over finite time from ambient to interior based on thermal insulation model and respective temps
2. Calculate heat flow over finite time to ambient from interior based on chiller performance and respective temps
3. Apply net heat flow to interior and calculate new interior temps and phases
4. Advance time step

# Transient full system loop
0. Initialize temperatures
1. Calculate heat flow over finite time from ambient to interior based on thermal insulation model and respective temps
2. Calculate heat flow over finite time to ambient from interior based on chiller performance and respective temps
3. Apply net heat flow to interior and calculate new interior temps and phases
5. Calculate power consumption of chiller
6. Calculate energy generation of solar
7. Apply net energy flow to battery status
8. Advance time step
