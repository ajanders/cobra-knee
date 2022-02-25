# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 13:44:09 2022

@author: Anthony Anderson

This script creates a knee flexion-extension moment plot for our ICORR 2022
conference paper.

This script displays the plot, which I then save as a .pdf file and import
into Affinity Designer to touch up and make publication-ready.

"""

import matplotlib.pyplot as plt
import numpy as np

from src import knee_data_processing as ferris

# %% Load Ferris data

# digitized knee moments from the literature
knee_moments = ferris.load_and_process_ferris_moments()

# extract data
phase = knee_moments['phase']
control = knee_moments['control']
esr = knee_moments['esr']
biom = knee_moments['biom']

# %% Generate candidate control signals

# create a function that generates example setpoints for the knee exoskeleton
# torque controller using the equation from a gaussian function

def torque_signal(peak, midpoint, width):

    phase = np.linspace(0, 1, 1000)
    signal = peak*np.exp(-((phase-midpoint)**2)/(2*width**2))

    return signal

# define a few control signals
t0 = torque_signal(peak=0.09375, midpoint=0.45, width=0.05)
t1 = torque_signal(peak=0.1875, midpoint=0.45, width=0.05)
t2 = torque_signal(peak=0.28125, midpoint=0.45, width=0.05)

# %% Create Plot

# plot setup
data_width = 4
colors = ['#1446A0','#DB3069', '#F5D547']

plt.figure()

# plot ferris data
plt.plot(phase, control, color=colors[0],
         linewidth=data_width, label='healthy control subjects')

plt.plot(phase, esr, color=colors[1],
         linewidth=data_width, label='energy storage and return prostheses')

plt.plot(phase, biom, color=colors[2],
         linewidth=data_width, label='BiOM robotic ankle prostheses')

# plot control signals
plt.plot(phase, t0, 'k', label='proposed exoskeleton assistance')
plt.plot(phase, t1, 'k')
plt.plot(phase, t2, 'k')

plt.xlabel('Gait Cycle (%)')
plt.ylabel('Knee Flexion  Moment (Nm/kg)')
plt.legend()
plt.xlim([0, 100])