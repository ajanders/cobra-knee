# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 07:23:12 2022

@author: Anthony Anderson

This is a primary analysis pipeline for work relating to the knee flexion
exoskeleton I've developed for transtibial amputees. The results will be
submitted to the International Conference on Rehabilitation Robotics in
February 2022.

This script loads experimental data, low-pass filters signals of interest,
segments gait cycles, and stores results in a dictionary that will be accessed
by other scripts that make figures. This script just lays out the pipeline by
calling functions, all of the heavy-lifting code is in the src folder.

"""

import pickle

from src import data_import as load
from src import filters
from src import gait_cycles
from src import averages
from src import results

# %% Import all files in the specified directory

# data is stored in 10-second long tdms files in the 'data' folder of the
# repo. Data is not available online due to current data-sharing rules at the
# VA.

participant = ['BP A 010']
data = load.import_multiple_participant_data(participant)

# %% Filter data

# apply a low-pass butterworth filter to some of the signals within the data.
# filter cutoff frequencies are in Hz.
filter_frequencies = {'GRFz (N)': 20,
                      'Exoskeleton Angle (deg)': 12,
                      'Joint Torque Setpoint (Nm)': 12,
                      'Joint Torque (Nm)': 12}

filters.filter_signals(data, filter_frequencies)

# %% Segment gait cycles

gait_cycles.segment_strides(data)

# %% Construct the average signal for each signal in each trial

averages.average_strides(data)

# %% Compute output metrics for paper

# compute peak torque, peak cable force, total range of motion over all trials
results.compute_outcomes(data)

# %% pickle data and store it

filename = '..//results//intermediate//main_gait_pipeline_pickle_output'
outfile = open(filename, 'wb')
pickle.dump(data, outfile)
outfile.close()
