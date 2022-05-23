# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 07:23:12 2022

@author: Anthony Anderson

This is a primary analysis pipeline for a walking experiment I conducted with
a knee flexion assist exoskeleton for people with transtibial amputation. This
script produces all results for the publication titled:
    
"Design and Evaluation of a Knee Flexion Assistance Exoskeleton for People with
Transtibial Amputation"

by Anthony J. Anderson, Yuri F. Hudak, Kira A. Gauthier, Brittney C. Muir, and
Patrick M. Aubin

The manuscript has been accepted to the 2022 International Conference on
Rehabilitation Robotics. 

This script loads experimental data, low-pass filters signals of interest,
segments gait cycles, and stores results in a pickle file that will be accessed
by other scripts to make figures. This script implements the analysis pipeline
by calling functions, all of the heavy-lifting code is in the src folder.

"""

import pickle

# import my packages from the src folder
from src import data_import as load
from src import filters
from src import gait_cycles
from src import averages
from src import results

# %% Import all files in the specified directory

"""
Data is stored in 10-second long TDMS files in the 'data' folder of the
repository. Data is not available online due to current data-sharing rules at
the Seattle VA Hospital, but will be uploaded in the future if possible.

This function loads all experimental data into a dictionary titled "data". The
data dictionary holds raw data for each trial as a Pandas DataFrame, as well
as metadata, file names, etc. Each subsequent function in this script modifies
the data dictionary with new processed types of data.

"""

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

# Segment the data in each file into individual strides using heel strikes
# and normalize in time so that each stride has an identical number of elements
gait_cycles.segment_strides(data)

# %% Construct the average signal for each signal in each trial

# Compute the mean stride for every signal in every file.
averages.average_strides(data)

# Compute the mean stride for every signal in every condition. I.e., each
# experimental condition has two corresponding files. This function merges the
# average strides across the appropriate files
averages.condition_averages(data)

# %% Compute output metrics for paper

# Compute outcomes that appear in the paper (tracking error, range of motion,
# peak torque, etc.)
results.compute_outcomes(data)

# %% pickle data and store it

# store the data in an intermediate location that can be accessed by other
# scripts for plotting and visualization. 

filename = '..//results//intermediate//main_gait_pipeline_pickle_output'
outfile = open(filename, 'wb')
pickle.dump(data, outfile)
outfile.close()
