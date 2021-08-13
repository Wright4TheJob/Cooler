import cooler.contents as cont
import cooler.insulation as ins
import cooler.chiller as chill
from cooler import utilities as utils
from icecream import ic
import numpy as np

def propogate_simulation_passive(insulator, contents, t_ambient=30, duration=60*60, time_step = 60):
    ts = np.arange(0,duration, time_step).tolist()
    temps = [contents.temp]
    liquids = [contents.liquid_fraction]
    t_ambients = [t_ambient]
    for i in ts[:-1]:
        delta_t = t_ambient - contents.temp
        inflow_energy = delta_t * insulator.get_conductance_kW_per_C() * time_step
        contents.change_energy(inflow_energy)
        temps.append(contents.temp)
        liquids.append(contents.liquid_fraction)
        t_ambients.append(t_ambient)

    return [ts, temps, liquids, t_ambients]

def propogate_simulation_chilled(insulator, contents, chiller, t_ambient=30, duration=2*60*60, time_step = 1):

    # Initialize data lists
    ts = np.arange(0,duration, time_step).tolist()
    temps = [contents.temp]
    liquids = [contents.liquid_fraction]
    duty_cycle = [0]
    if contents.temp > chiller.t_target:
        duty_cycle[0] = 1
    t_ambients = [t_ambient]

    # Simulation loop
    for i in ts[:-1]:
        delta_t = t_ambient - contents.temp
        inflow_energy = delta_t * insulator.get_conductance_kW_per_C() * time_step
        outflow_energy = chiller.get_Q_kW_for_temps(t_ambient, contents.temp)
        delta_e = inflow_energy - outflow_energy
        contents.change_energy(delta_e)
        temps.append(contents.temp)
        liquids.append(contents.liquid_fraction)

        if outflow_energy <= 0:
            duty_cycle.append(0)
        else:
            duty_cycle.append(1)
        t_ambients.append(t_ambient)

    return [ts, temps, liquids, duty_cycle, t_ambients]

def propogate_simulation_chilled_weather(insulator, contents, chiller, weather_filename, time_step = 60):
    # Import weather data
    with open(weather_file, newline='') as csvfile:
        w = weather.Weather(csvfile)
    duration = weather.seconds_between(w.start_date, w.end_date)
    offset = 0
    w.temps = [t + offset for t in w.temps]

    # Initialize data lists
    ts = np.arange(0, duration, time_step).tolist()
    temps = [contents.temp]
    liquids = [contents.liquid_fraction]
    duty_cycle = [0]
    if contents.temp > chiller.t_target:
        duty_cycle[0] = 1
    t_ambs = [t_ambient]
    t_ambs[0] = w.temps[0]

    # Simulation loop
    for i in ts[:-1]:
        time = w.start_date + timedelta(0,i)
        t_ambient = w.temp_at_datetime(time)

        delta_t = t_ambient - contents.temp
        inflow_energy = delta_t * insulator.get_conductance_kW_per_C() * time_step
        chiller_q = chiller.get_Q_kW_for_temps(t_ambient, contents.temp)
        outflow_energy = chiller_q* time_step

        delta_e = inflow_energy - outflow_energy
        contents.change_energy(delta_e)
        temps.append(contents.temp)
        liquids.append(contents.liquid_fraction)
        if chiller_q <= 0:
            duty_cycle.append(0)
        else:
            duty_cycle.append(1)
        t_ambs.append(t_ambient)

    returns = [ts, temps, liquids, duty_cycle, t_ambs]
    return returns

# Initialize Contents
contents = cont.Water(mass=10, temp=-5)

# Initialize Insulator
box = ins.Box()
box.set_insulation_k(1)
box.set_height(1)
box.set_width(1)
box.set_length(1)
box.set_insulation_thick(0.2)

# Initialize Chiller
tec = chill.Chiller()
tec.set_type("tec")
tec.set_thermostat(5)
tec.add_performance_data_point(0, 500, 0)
tec.add_performance_data_point(0, 0, 1000)

# Run the simulation
[xs, temps, liquids, t_ambient] = propogate_simulation_passive(box, contents)
[xs, temps, liquids, duty_cycle, t_ambient] = propogate_simulation_chilled(box, contents, tec)

# Clean up data for plotting
avg_duty_cycles = utils.moving_average(duty_cycle, window=20)
avg_duty_cycles = [x*100 for x in avg_duty_cycles]
liquids = [x*100 for x in liquids]

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

fig, ax1 = plt.subplots()
ax1.plot(xs, temps, 'k', label='Simulated Temp')
ax1.plot(xs, t_ambient, 'g', label='Ambient Temp')
ax1.set_ylabel('Temperature [C]')
ax1.set_xlabel('Time [s]')
#xfmt = mdates.DateFormatter('%H:%M')
#ax1.xaxis.set_major_formatter(xfmt)

#ax.plot(xs, liquids, 'r:', label='Liquid Fraction')
ax2 = ax1.twinx()
ax2.plot(xs, avg_duty_cycles, 'b', label='Duty Cycle')
ax2.plot(xs, liquids, 'r-', label='Liquid Fraction')
ax2.set_ylabel('Duty Cycle', color='k')
ax2.tick_params('y')
ax2.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
#ax2.xaxis.set_major_formatter(xfmt)

legend = fig.legend()

plt.show()
print("Maximum contents temperature: %2.2f C"%(max(temps)))
print("Average model error: %2.4f"%(avg_model_error))
print("SSE: %2.3f"%(SSE))
