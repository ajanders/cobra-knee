# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 10:27:59 2022

@author: antho
"""

import numpy as np
import matplotlib.pyplot as plt

from src import data_import as load
from src import filters
from src import gait_cycles
from src import averages

# %% Import all files in the specified directory

# data is stored in 10-second long tdms files in the 'data' folder of the
# repo. Data is not available online for data-sharing rules at the VA.

participant = ['anthony static']
data = load.import_multiple_participant_data(participant)

# %% Extract a perturbation

trial = data['anthony static']['raw signals']['Perturb30Deg']

time = np.linspace(0, 10, 10000)
vel = trial['Motor Velocity (deg/s)']
pos = trial['Motor Position (deg)'] - trial['Motor Position (deg)'][0]
torque = trial['Joint Torque (Nm)']
setpoint = trial['Joint Torque Setpoint (Nm)']

fig, axes = plt.subplots(3, 1)
axes[0].plot(time, vel, 'C0', linewidth=3)
axes[0].set_ylabel('Motor Velocity (deg/s)')
axes[1].plot(time, pos, 'C2', linewidth=3)
axes[1].set_ylabel('Motor Position (deg)')
axes[2].plot(time, setpoint, 'k--', linewidth=3)
axes[2].plot(time, torque, 'r', linewidth=3)
axes[2].set_ylabel('Exoskeleton Torque (Nm)')
axes[2].set_xlabel('Time (s)')