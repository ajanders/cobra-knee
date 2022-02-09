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

import numpy as np
import matplotlib.pyplot as plt

from src import data_import as load
from src import filters

# %% Import all files in the specified directory

# data is stored in 10-second long tdms files in the 'data' folder of the
# repo. Data is not available online for data-sharing rules at the VA.

participant = ['anthony static']
data = load.import_multiple_participant_data(participant)

# %% Filter data

# apply a low-pass butterworth filter to some of the signals within the data.
# filter cutoff frequencies are in Hz
filter_frequencies = {'GRFz (N)': 20,
                      'Exoskeleton Angle (deg)': 12}

filters.filter_signals(data, filter_frequencies)

# %%
