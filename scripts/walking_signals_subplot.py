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

# extract the filtered signals from the data structure
filt_data = data['BP A 010']['filtered signals']

# extract trial that will be plotted
filename = 'high_0'
trial = filt_data[filename]

# extract signals
time = np.linspace(0, 10, 10000)
grf = trial['GRFz (N)'].values
phase = trial['Gait Phase (%)']*100
angle = trial['Exoskeleton Angle (deg)']
setpoint = trial['Joint Torque Setpoint (Nm)']
torque = trial['Joint Torque (Nm)']

# add offset to angle, measured in office after data collection was over
offset = 73.4
angle = angle + offset

# %% Create plot

# subplot with four rows, one column
fig, axes = plt.subplots(4, 1)

# color palatte was generated using coolors.co
colors = ['#2B2D42', '#FF66D8', '#20A39E']
w = 3

axes[0].plot(time, grf, linewidth=w, color=colors[0])
axes[0].set_ylabel('GRFz (N)')

axes[1].plot(time, phase, color=colors[1], linewidth=w)
axes[1].set_ylabel('Phase (%)')

axes[2].plot(time, angle, color=colors[2], linewidth=w)
axes[2].set_ylabel('Exoskeleton\nAngle (deg)')

axes[3].plot(time, setpoint, 'k--', linewidth=w)
axes[3].plot(time, torque, 'r', linewidth=w)
axes[3].set_ylabel('Exoskeleton\nTorque (Nm)')
axes[3].set_xlabel('Time (s)')
