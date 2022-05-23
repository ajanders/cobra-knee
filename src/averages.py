# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:28:23 2021

@author: Anthony Anderson

This set of functions is used merge and combine data when taking averages
1) across strides within a single trial and 2) over signals across conditions.

The main_gait_pipeline.py script calls the "average_strides" function and the
"condition_averages" function.

The average_strides function compute the mean signal (and standard deviation)
for each stride over each file. For example, given a file with 10 strides and
four measurements, the function condenses the 10 strides down to a single
average for each of the four measurements. 

The condition_averages goes one step further, and merges specific files
together that represent the same experimental condition.

"""

import numpy as np
import pandas as pd

# %% compute average strides for a single file/trial

def trial_average_strides(trial):
    """
    For a single trial, compute the mean and standard deviation trajectories
    for each signal of interest. 

    Parameters
    ----------
    trial : dictionary
        This dictionary contains Pandas DataFrames that hold segmented, time
        normalized strides for four signals of interest. On average, each
        trial contains 9-10 strides. Signals are exoskeleton angle, ground
        reaction force, joint torque, and joint torque setpoint.

    Returns
    -------
    trial_averages : dictionary
        Dictionary where signal names are keys, and values are Pandas
        DataFrames with two columns. First column is 'Mean' and second column
        is 'SD'.

    """
    
    # create new data structure to hold average signals
    trial_averages = {}

    # we'll store average data in a pandas DataFrame with these
    # columns:
    column_headers = ['Mean', 'SD']

    # now loop through signals
    for signal_name in trial:

        # extract all strides as an array where each column is a stride
        strides_array = trial[signal_name].values

        # compute averages and standard deviations over the columns
        average_stride = np.mean(strides_array, axis=1)
        sd_stride = np.std(strides_array, axis=1)

        # add mean and sd arrays to a single array and put in DataFrame
        average_array = np.column_stack((average_stride, sd_stride))
        df = pd.DataFrame(data=average_array, columns=column_headers)

        # put the DataFrame in a dictionary where the file name is the
        # key
        trial_averages[signal_name] = df
    
    return trial_averages

# %% all participants

def average_strides(data):
    """
    Compute the mean signal (and standard deviation) for each stride over each
    file.

    Parameters
    ----------
    data : dictionary
        This is the primary data structure in the main gait processing
        pipeline.

    Returns
    -------
    None. An 'averages' key is added to the input data structure in place, and
    maps to further dictionaries/dataframes with mean and sd signals for each
    trial.

    """

    # loop over each participant in the data set
    for participant in data:
        
        # extract data structure for this participant
        participant_data = data[participant]
        
        # extract the normalized 'strides' data structure from the participant
        # data structure
        stride_data = participant_data['strides']

        # create a dictionary container for average strides for all files
        averages = {}

        # loop through each signal within each file and compute means and sd's
        for file_name in stride_data:

            # compute mean and sd for all signals in this trial
            trial_averages = trial_average_strides(stride_data[file_name])

            # once all signals have been iterated over, put the averages for
            # all signals in a dictionary where the file name is the key
            averages[file_name] = trial_averages

        # after all files have been iterated over, store the complete output
        # under the key 'averages
        participant_data['averages'] = averages

    return None

# %% function to compute average two signals

def mean_signal(signal_0, signal_1):
    return (signal_0+signal_1)/2

# %% 

def merge_trials(averages, file_name_0, file_name_1):
    """
    Given average trajectories and two file names that refer to files with
    the same experimental condition, return the overall average signals for
    that condition.

    Parameters
    ----------
    averages : dictionary
        Dictionary where file names are keys, and values are sub-dictionaries
        containing signal names and means and sds.
    file_name_0 : string
        first file to combine.
    file_name_1 : string
        second file to combine.

    Returns
    -------
    merged_dict : dictionary
        Signal names map to sub-dictionaries with keys 'mean' and 'sd'
        trajectories.

    """
    
    trial_0 = averages[file_name_0]
    trial_1 = averages[file_name_1]
    
    merged_dict = {}
    
    for signal_name in trial_0:
        
        signal_0_mean = trial_0[signal_name]['Mean']
        signal_1_mean = trial_1[signal_name]['Mean']
        
        signal_0_sd = trial_0[signal_name]['SD']
        signal_1_sd = trial_1[signal_name]['SD']
        
        mean = mean_signal(signal_0_mean, signal_1_mean)
        sd = mean_signal(signal_0_sd, signal_1_sd)
        
        merged_dict[signal_name] = {'Mean': mean, 'SD': sd}
    
    return merged_dict

# %% compute means and sd's across conditions

def condition_averages(data):
    """
    After the mean and standard deviation trajectories have been computed for
    every trial/file, we need to further average across files that correspond
    to the same experimental condition.

    Parameters
    ----------
    data : dict
        This is the primary data dictionary that is operated on by all other
        functions in this pipeline.

    Returns
    -------
    None. data is modified in place with a key for 'conditions'.

    """
    
    # extract average strides
    averages = data['BP A 010']['averages']

    # compute mean and SD for each signal across strides
    transparent = merge_trials(averages, 'transparent_0', 'transparent_1')
    low = merge_trials(averages, 'low_0', 'low_1')
    med = merge_trials(averages, 'med_0', 'med_1')
    high = merge_trials(averages, 'high_0', 'high_1')
    
    data['BP A 010']['averages']['conditions'] = {'transparent': transparent,
                                                  'low': low,
                                                  'medium': med,
                                                  'high': high}
    
    return None
    
    