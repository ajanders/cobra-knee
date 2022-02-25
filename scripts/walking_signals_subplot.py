# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:50:30 2022

@author: Anthony Anderson

This script creates a subplot of several walking signals for our ICORR 2022
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

# %% Extract data

# define the file that will be plotted
filename = 'high_0'

# extract the raw signals from the data structure
trial_raw = data['BP A 010']['raw signals'][filename]

# get the phase signal
phase = trial_raw['Gait Phase (%)']

# extract the filtered signals from the data structure
trial_filtered = data['BP A 010']['filtered signals'][filename]

# extract filtered signals for the plot
grf = trial_filtered['GRFz (N)']
angle = trial_filtered['Exoskeleton Angle (deg)']
setpoint = trial_filtered['Joint Torque Setpoint (Nm)']
torque = trial_filtered['Joint Torque (Nm)']

# add offset to angle, measured in office after data collection was over
offset = 73.4
angle = angle + offset

# define time
time = np.linspace(0, 10, 10000)

# %% Create plot

# subplot with four rows, one column
fig, axes = plt.subplots(4, 1)

# color palatte was generated using coolors.co
colors = ['#2B2D42', '#FF66D8', '#20A39E']
w = 3

axes[0].plot(time, grf, linewidth=w, color=colors[0])
axes[0].set_ylabel('GRFz (N)')

axes[1].plot(time, phase, color=colors[1], linewidth=w)
axes[1].set_ylabel('Gait\nPhase (%)')

axes[2].plot(time, angle, color=colors[2], linewidth=w)
axes[2].set_ylabel('Exoskeleton\nAngle (deg)')

axes[3].plot(time, setpoint, 'k--', linewidth=w)
axes[3].plot(time, torque, 'r', linewidth=w)
axes[3].set_ylabel('Exoskeleton\nTorque (Nm)')
axes[3].set_xlabel('Time (s)')
