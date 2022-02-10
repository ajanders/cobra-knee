# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 09:02:07 2022

@author: Claudius
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

participant = ['anthony walking']
data = load.import_multiple_participant_data(participant)

filter_frequencies = {'Joint Torque (Nm)': 20,
                      'GRFz (N)': 20}
filters.filter_signals(data, filter_frequencies)

gait_cycles.strides(data)

# %% Extract a perturbation

# file = 'perturb_off_170deg_0'
# file = 'perturb_off_170deg_1'
# file = 'perturb_off_170deg_2'
# file = 'perturb_off_190deg_0'
# file = 'perturb_off_190deg_1'
# file = 'perturb_on_40deg_0'
# file = 'perturb_on_40deg_1'
# file = 'perturb_on_60deg_0'
# file = 'perturb_on_60deg_1'

# trial = data['anthony walking']['raw signals'][file]

# time = np.linspace(0, 10, 10000)
# vel = trial['Motor Velocity (deg/s)']
# pos = trial['Motor Position (deg)'] - trial['Motor Position (deg)'][0]
# torque = trial['Joint Torque (Nm)']
# setpoint = trial['Joint Torque Setpoint (Nm)']

# fig, axes = plt.subplots(3, 1)
# axes[0].plot(time, vel, 'C0', linewidth=3)
# axes[0].set_ylabel('Motor Velocity (deg/s)')
# axes[0].set_title(file)
# axes[1].plot(time, pos, 'C2', linewidth=3)
# axes[1].set_ylabel('Motor Position (deg)')
# axes[2].plot(time, setpoint, 'k--', linewidth=3)
# axes[2].plot(time, torque, 'r', linewidth=3)
# axes[2].set_ylabel('Exoskeleton Torque (Nm)')
# axes[2].set_xlabel('Time (s)')

# %% look at strides

file_off = 'perturb_off_190deg_1'
file_on = 'perturb_on_60deg_1'

phase = np.linspace(0, 100, 500)

trial_off = data['anthony walking']['strides'][file_off]
trial_on = data['anthony walking']['strides'][file_on]


# algorithm for determining a torque perturbation

"""

We have an array of time normalized strides, where each stride is a column.
I want to find the column with the perturbation, then take the average of all
other columns EXCEPT for the stride immediately following the perturbation.


"""

def get_average_nonperturbed_stride(stride_array):

    # get max of each column
    column_maxes = np.max(stride_array, axis=0)

    # get index of column with perturbation
    pert_column = np.argmax(column_maxes)

    # get column after perturbation
    after = pert_column+1

    # make a copy and delete the columns
    non_perturbed = np.copy(stride_array)
    non_perturbed = np.delete(non_perturbed, [pert_column, after], axis=1)

    # perturbed array
    perturbed = stride_array[:,pert_column]

    # average of non perturbed
    non_perturbed_mean = np.mean(non_perturbed, axis=1)

    # define torque perturbation
    torque_perturbation = perturbed - non_perturbed_mean

    return torque_perturbation, perturbed, non_perturbed_mean

# %% get em

torque_perturbation_off, perturbed_off, non_perturbed_mean_off = get_average_nonperturbed_stride(trial_off['Joint Torque (Nm)'].values)
grf_perturbation_off, perturbed_grf_off, non_perturbed_grf_mean_off = get_average_nonperturbed_stride(trial_off['GRFz (N)'].values)

torque_perturbation_on, perturbed_on, non_perturbed_mean_on = get_average_nonperturbed_stride(trial_on['Joint Torque (Nm)'].values)
grf_perturbation_on, perturbed_grf_on, non_perturbed_grf_mean_on = get_average_nonperturbed_stride(trial_on['GRFz (N)'].values)


fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].set_title('Exoskeleton in Transparent Mode')
axes[0].plot(phase, trial_off['Joint Torque (Nm)'])
axes[0].plot(phase, perturbed_off, 'k-', label='Perturbed stride')
axes[0].plot(phase, non_perturbed_mean_off, 'k-.', label='Mean of non-perturbed strides')
axes[0].plot(phase, torque_perturbation_off, 'r', linewidth=3, label='Perturbation')
axes[0].set_ylabel('Exoskeleton Torque (Nm)')
axes[0].legend()

axes[1].plot(phase, trial_off['GRFz (N)'])
axes[1].plot(phase, perturbed_grf_off, 'k-')
axes[1].plot(phase, non_perturbed_grf_mean_off, 'k-.')
axes[1].plot(phase, grf_perturbation_off, 'r', linewidth=3)
axes[1].set_ylabel('Ground Reaction Force (N)')

fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].set_title('Exoskeleton in Active Mode')
axes[0].plot(phase, trial_on['Joint Torque (Nm)'])
axes[0].plot(phase, perturbed_on, 'k-', label='Perturbed stride')
axes[0].plot(phase, non_perturbed_mean_on, 'k-.', label='Mean of non-perturbed strides')
axes[0].plot(phase, torque_perturbation_on, 'r', linewidth=3, label='Perturbation')
axes[0].set_ylabel('Exoskeleton Torque (Nm)')

axes[1].plot(phase, trial_on['GRFz (N)'])
axes[1].plot(phase, perturbed_grf_on, 'k-')
axes[1].plot(phase, non_perturbed_grf_mean_on, 'k-.')
axes[1].plot(phase, grf_perturbation_on, 'r', linewidth=3)
axes[1].set_ylabel('Ground Reaction Force (N)')


