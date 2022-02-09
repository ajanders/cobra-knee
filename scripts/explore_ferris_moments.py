# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 13:44:09 2022

@author: Anthony Anderson


"""

import matplotlib.pyplot as plt
import numpy as np

from src import knee_data_processing as ferris

# %% Load Ferris data

knee_moments = ferris.load_and_process_ferris_moments()

# extract data
phase = knee_moments['phase']/100
control = knee_moments['control']
esr = knee_moments['esr']
biom = knee_moments['biom']

# %% Function to generate candidate control signals

def torque_signal(peak, midpoint, width):
    
    phase = np.linspace(0, 1, 1000)
    signal = peak*np.exp(-((phase-midpoint)**2)/(2*width**2))
    
    return signal

# define a few control signals 
t0 = torque_signal(peak=0.0625, midpoint=0.45, width=0.05)
t1 = torque_signal(peak=0.125, midpoint=0.45, width=0.05)
t2 = torque_signal(peak=0.1875, midpoint=0.45, width=0.05)
t3 = torque_signal(peak=0.25, midpoint=0.45, width=0.05)
t4 = torque_signal(peak=0.3125, midpoint=0.45, width=0.05)
t5 = torque_signal(peak=0.375, midpoint=0.45, width=0.05)


# %% Create Plot

# plot setup
data_width = 4
colors = ['#1446A0','#DB3069', '#F5D547']

plt.figure()

# plot ferris data
plt.plot(phase, control, color=colors[0],
         linewidth=data_width, label='Healthy Control Subjects')

plt.plot(phase, esr, color=colors[1],
         linewidth=data_width, label='Energy Storage and Return Foot')

plt.plot(phase, biom, color=colors[2],
         linewidth=data_width, label='Biom')

# plot control signals
plt.plot(phase, t0, 'k--', label='Proposed exoskeleton assistance')
plt.plot(phase, t1, 'k--')
plt.plot(phase, t2, 'k--')
plt.plot(phase, t3, 'k--')
plt.plot(phase, t4, 'k--')
plt.plot(phase, t5, 'k--')

plt.xlabel('Gait Cycle (%)')
plt.ylabel('Knee Flexion  Moment (Nm/kg)')
plt.legend()