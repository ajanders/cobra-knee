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

from src import knee_data_processing as ferris

# %% Load Ferris data

knee_moments = ferris.load_and_process_ferris_moments()

# extract data
phase_ferris = knee_moments['phase']
control = knee_moments['control']

# %% Load experimental data from storage

filename = '..//results//intermediate//main_gait_pipeline_pickle_output'
infile = open(filename, 'rb')
data = pickle.load(infile)
infile.close()

# %% Extract plot data

# extract average strides
average_strides = data['BP A 010']['averages']

# extract phase
phase_trans = (average_strides['transparent_0']['Gait Phase (%)']['Mean'] + average_strides['transparent_0']['Gait Phase (%)']['Mean'])/2
phase_low = (average_strides['low_0']['Gait Phase (%)']['Mean'] + average_strides['low_1']['Gait Phase (%)']['Mean'])/2
phase_med = (average_strides['med_0']['Gait Phase (%)']['Mean'] + average_strides['med_1']['Gait Phase (%)']['Mean'])/2
phase_high = (average_strides['high_0']['Gait Phase (%)']['Mean'] + average_strides['high_1']['Gait Phase (%)']['Mean'])/2

# extract setpoints for different modes
setpoint_transparent = (average_strides['transparent_0']['Joint Torque Setpoint (Nm)']['Mean'] + average_strides['transparent_0']['Joint Torque Setpoint (Nm)']['Mean'])/2
setpoint_low = (average_strides['low_0']['Joint Torque Setpoint (Nm)']['Mean'] + average_strides['low_1']['Joint Torque Setpoint (Nm)']['Mean'])/2
setpoint_medium = (average_strides['med_0']['Joint Torque Setpoint (Nm)']['Mean'] + average_strides['med_1']['Joint Torque Setpoint (Nm)']['Mean'])/2
setpoint_high = (average_strides['high_0']['Joint Torque Setpoint (Nm)']['Mean'] + average_strides['high_1']['Joint Torque Setpoint (Nm)']['Mean'])/2

# extract torque for the same
torque_transparent = (average_strides['transparent_0']['Joint Torque (Nm)']['Mean'] + average_strides['transparent_1']['Joint Torque (Nm)']['Mean'])/2
torque_low = (average_strides['low_0']['Joint Torque (Nm)']['Mean'] + average_strides['low_1']['Joint Torque (Nm)']['Mean'])/2
torque_med = (average_strides['med_0']['Joint Torque (Nm)']['Mean'] + average_strides['med_1']['Joint Torque (Nm)']['Mean'])/2
torque_high = (average_strides['high_0']['Joint Torque (Nm)']['Mean'] + average_strides['high_1']['Joint Torque (Nm)']['Mean'])/2

# extract standard deviations for torque
torque_transparent_SD = (average_strides['transparent_0']['Joint Torque (Nm)']['SD'] + average_strides['transparent_1']['Joint Torque (Nm)']['SD'])/2
torque_low_SD = (average_strides['low_0']['Joint Torque (Nm)']['SD'] + average_strides['low_1']['Joint Torque (Nm)']['SD'])/2
torque_med_SD = (average_strides['med_0']['Joint Torque (Nm)']['SD'] + average_strides['med_1']['Joint Torque (Nm)']['SD'])/2
torque_high_SD = (average_strides['high_0']['Joint Torque (Nm)']['SD'] + average_strides['high_1']['Joint Torque (Nm)']['SD'])/2

# create x-axis data
phase = np.linspace(0, 100, len(torque_low_SD))

# %% Create plot

# define colors
colors = ['#FFBF00', '#F15152', '#662E9B', '#048BA8']

plt.figure()

plt.plot(phase_ferris, control*83.6, 'k', alpha=0.25, linewidth=4)

plt.plot(phase, setpoint_low, 'k--', label='setpoint')
plt.plot(phase, setpoint_medium, 'k--')
plt.plot(phase, setpoint_high, 'k--')
plt.plot(phase, setpoint_transparent, 'k--')

# plot transparent standard deviation bounds for exoskeleton torque
plt.fill_between(phase, torque_transparent-torque_transparent_SD, torque_transparent+torque_transparent_SD,
                 color=colors[0], alpha=0.4)
plt.fill_between(phase, torque_low-torque_low_SD, torque_low+torque_low_SD,
                 color=colors[1], alpha=0.4)
plt.fill_between(phase, torque_med-torque_med_SD, torque_med+torque_med_SD,
                 color=colors[2], alpha=0.4)
plt.fill_between(phase, torque_high-torque_high_SD, torque_high+torque_high_SD,
                 color=colors[3], alpha=0.4)

plt.plot(phase, torque_transparent, color=colors[0], linewidth=4, label='transparent')
plt.plot(phase, torque_low, color=colors[1], linewidth=4, label='a=7.84 Nm')
plt.plot(phase, torque_med, color=colors[2], linewidth=4, label='a=15.68 Nm')
plt.plot(phase, torque_high, color=colors[3], linewidth=4, label='a=23.51 Nm')

plt.xlabel('Gait Cycle (%)')
plt.ylabel('Exoskeleton Torque (Nm)')
plt.legend()
plt.xlim([0, 100])
plt.ylim([-7.5, 42])