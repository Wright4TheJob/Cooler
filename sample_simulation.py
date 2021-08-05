import chiller.contents as cont
import chiller.insulation as ins
import chiller.chiller as chill
from icecream import ic

def propogate_sim(insulator, contents, chiller=None, t_ambient=30, duration=60*60, time_step = 60):
    import numpy as np
    ts = np.arange(0,duration, time_step).tolist()
    temps = [contents.temp]
    liquids = [contents.liquid_fraction]
    for i in ts[:-1]:
        delta_t = t_ambient - contents.temp
        inflow_energy = delta_t * insulator.get_conductance_kW_per_C() * time_step
        if chiller:
            outflow_energy = chiller.heat_removed(delta_t)
        else:
            outflow_energy = 0
        delta_e = inflow_energy - outflow_energy
        c.change_energy(delta_e)
        temps.append(contents.temp)
        liquids.append(contents.liquid_fraction)

    return ts, temps, liquids

c = cont.Water(mass=10, temp=-5)

box = ins.Box()
box.set_insulation_k(1)
box.set_height(2)
box.set_width(2)
box.set_length(2)
box.set_insulation_thick(0.2)

tec = chill.Chiller()
tec.set_type("tec")
t_ambient = 20
t_contents = 10
tec.add_performance_data_point(20, 0)
tec.add_performance_data_point(0, 50)

xs, temps, liquids = propogate_sim(box, c)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(xs, temps, 'k', label='Temperature')
ax.plot(xs, liquids, 'r:', label='Liquid Fraction')
legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
legend.get_frame().set_facecolor('C0')
plt.show()
