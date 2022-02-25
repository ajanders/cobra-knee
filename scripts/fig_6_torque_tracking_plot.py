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

# load knee moments digitized from citation [4] in our paper
knee_moments = ferris.load_and_process_ferris_moments()

# extract data
phase_ferris = knee_moments['phase']
control = knee_moments['control']*83.6

# %% Load experimental data from storage

# This loads the pickle output of the "main_gait_pipeline.py" program.

filename = '..//results//intermediate//main_gait_pipeline_pickle_output'
infile = open(filename, 'rb')
data = pickle.load(infile)
infile.close()

# %% function to average two signals

def mean_signal(signal_0, signal_1):
    return (signal_0+signal_1)/2

# %% Extract plot data

# extract average strides
average_strides = data['BP A 010']['averages']

# extract setpoints for different modes
setpoint_trans_0 = average_strides['transparent_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_trans_1 = average_strides['transparent_1']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_transparent = mean_signal(setpoint_trans_0, setpoint_trans_1)

setpoint_low_0 = average_strides['low_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_low_1 = average_strides['low_1']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_low = mean_signal(setpoint_low_0, setpoint_low_1)

setpoint_med_0 = average_strides['med_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_med_1 = average_strides['med_1']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_med = mean_signal(setpoint_med_0, setpoint_med_1)

setpoint_high_0 = average_strides['high_0']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_high_1 = average_strides['high_1']['Joint Torque Setpoint (Nm)']['Mean']
setpoint_high = mean_signal(setpoint_high_0, setpoint_high_1)

# extract torque signals for the same
torque_trans_0 = average_strides['transparent_0']['Joint Torque (Nm)']['Mean']
torque_trans_1 = average_strides['transparent_1']['Joint Torque (Nm)']['Mean']
torque_transparent = mean_signal(torque_trans_0, torque_trans_1)

torque_low_0 = average_strides['low_0']['Joint Torque (Nm)']['Mean']
torque_low_1 = average_strides['low_1']['Joint Torque (Nm)']['Mean']
torque_low = mean_signal(torque_low_0, torque_low_1)

torque_med_0 = average_strides['med_0']['Joint Torque (Nm)']['Mean']
torque_med_1 = average_strides['med_1']['Joint Torque (Nm)']['Mean']
torque_med = mean_signal(torque_med_0, torque_med_1)

torque_high_0 = average_strides['high_0']['Joint Torque (Nm)']['Mean']
torque_high_1 = average_strides['high_1']['Joint Torque (Nm)']['Mean']
torque_high = mean_signal(torque_high_0, torque_high_1)

# extract standard deviations for torque
torque_trans_0_sd = average_strides['transparent_0']['Joint Torque (Nm)']['SD']
torque_trans_1_sd = average_strides['transparent_1']['Joint Torque (Nm)']['SD']
torque_transparent_sd = mean_signal(torque_trans_0_sd, torque_trans_1_sd)

torque_low_0_sd = average_strides['low_0']['Joint Torque (Nm)']['SD']
torque_low_1_sd = average_strides['low_1']['Joint Torque (Nm)']['SD']
torque_low_sd = mean_signal(torque_low_0_sd, torque_low_1_sd)

torque_med_0_sd = average_strides['med_0']['Joint Torque (Nm)']['SD']
torque_med_1_sd = average_strides['med_1']['Joint Torque (Nm)']['SD']
torque_med_sd = mean_signal(torque_med_0_sd, torque_med_1_sd)

torque_high_0_sd = average_strides['high_0']['Joint Torque (Nm)']['SD']
torque_high_1_sd = average_strides['high_1']['Joint Torque (Nm)']['SD']
torque_high_sd = mean_signal(torque_high_0_sd, torque_high_1_sd)

# create x-axis data
phase = np.linspace(0, 100, len(torque_low_sd))

# %% Create plot

# define colors
colors = ['#FFBF00', '#F15152', '#662E9B', '#048BA8']

plt.figure()

plt.plot(phase_ferris, control, 'k', alpha=0.25, linewidth=4)

plt.plot(phase, setpoint_low, 'k--', label='setpoint')
plt.plot(phase, setpoint_med, 'k--')
plt.plot(phase, setpoint_high, 'k--')
plt.plot(phase, setpoint_transparent, 'k--')

# plot transparent standard deviation bounds for exoskeleton torque
plt.fill_between(phase, torque_transparent-torque_transparent_sd,
                 torque_transparent+torque_transparent_sd,
                 color=colors[0], alpha=0.4)

plt.fill_between(phase, torque_low-torque_low_sd, torque_low+torque_low_sd,
                 color=colors[1], alpha=0.4)

plt.fill_between(phase, torque_med-torque_med_sd, torque_med+torque_med_sd,
                 color=colors[2], alpha=0.4)

plt.fill_between(phase, torque_high-torque_high_sd, torque_high+torque_high_sd,
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