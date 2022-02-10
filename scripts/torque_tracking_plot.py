# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:35:30 2022

@author: Anthony Anderson

This script creates a knee exoskeleton torque-tracking plot for our ICORR 2022
conference paper.

This script displays the plot, which I then save as a .pdf file and import
into Affinity Designer to touch up and make publication-ready.

"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

# %% Load data from storage

filename = '..//results//intermediate//main_gait_pipeline_pickle_output'
infile = open(filename, 'rb')
data = pickle.load(infile)
infile.close()

# %% Extract plot data

# extract average strides
average_strides = data['anthony walking']['averages']

# extract setpoints for 5, 10, 15, 20, 25, 30
setpoint_0Nm = average_strides['exo_off_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_15Nm = average_strides['exo_on_15Nm_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_30Nm = average_strides['exo_on_30Nm_0']['Joint Torque Setpoint (Nm)']['Mean']

# extract torque for the same
torque_0Nm = average_strides['exo_off_0']['Joint Torque (Nm)']['Mean']
torque_15Nm = average_strides['exo_on_15Nm_0']['Joint Torque (Nm)']['Mean']
torque_30Nm = average_strides['exo_on_30Nm_0']['Joint Torque (Nm)']['Mean']

# extract standard deviations for torque
torque_0Nm_SD = average_strides['exo_off_0']['Joint Torque (Nm)']['SD']
torque_15Nm_SD = average_strides['exo_on_15Nm_0']['Joint Torque (Nm)']['SD']
torque_30Nm_SD = average_strides['exo_on_30Nm_0']['Joint Torque (Nm)']['SD']

# create x-axis data
phase = np.linspace(0, 100, len(torque_0Nm))

# %% Create plot

# define colors
colors = ['#F15152', '#662E9B', '#048BA8']

plt.figure()

plt.plot(phase, setpoint_0Nm, 'k--', label='setpoints')
plt.plot(phase, setpoint_15Nm, 'k--')
plt.plot(phase, setpoint_30Nm, 'k--')

# plot transparent standard deviation bounds for exoskeleton torque
plt.fill_between(phase, torque_0Nm-torque_0Nm_SD, torque_0Nm+torque_0Nm_SD,
                 color=colors[0], alpha=0.4)
plt.fill_between(phase, torque_15Nm-torque_15Nm_SD, torque_15Nm+torque_15Nm_SD,
                 color=colors[1], alpha=0.4)
plt.fill_between(phase, torque_30Nm-torque_30Nm_SD, torque_30Nm+torque_30Nm_SD,
                 color=colors[2], alpha=0.4)

plt.plot(phase, torque_0Nm, color=colors[0], linewidth=4, label='transparent')
plt.plot(phase, torque_15Nm, color=colors[1], linewidth=4, label='15 Nm peak')
plt.plot(phase, torque_30Nm, color=colors[2], linewidth=4, label='30 Nm peak')
plt.xlabel('Gait Cycle (%)')
plt.ylabel('Exoskeleton Torque (Nm)')
plt.legend()