# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:11:59 2021

@author: Anthony Anderson

This file contains functions used to chop signals into individual strides and
normalize them in time. I.e., given a ten-second recording of five signals,
return a structure that contains all five signals chopped into individual
strides, where each stride is a uniform vector length.

There are five functions in this file that work together:
    
    1.  "strides" is the highest level function that calls all other functions
        to get strides for every participant and every trial and every signal.
        This is the function that gets called by the primary processing
        pipeline.
        
    2.  "trial_strides" extracts variable-length strides over all signals
        in a given trial.
        
    3.  "get_stride_list" is a low-level function that chops a single signal
        into strides and returns the non-uniform strides in a list.
        
    4.  "normalize_trial_strides" normalizes all strides in a trial to a
        uniform length of 500 using interpolation.
        
    5.  "package_strides" is a convenience function that puts all strides into
        a dataframes with headers that list the stride number (e.g. "stride 1")
        and stores the strides in a dictionary that can be accessed by signal
        name. 

"""

import numpy as np
import pandas as pd

# %% get_stride_list

def get_stride_list(signal, heel_strike_indices):
    """
    Given a measurement (e.g. ground reaction force) and an array/list of
    heel-strike indices, chop out the individual strides from the signal and
    store them as variable length arrays inside of a list.

    Parameters
    ----------
    signal : ndarray
        Measurement of interest stored in an array.
    heel_strike_indices : ndarray
        List or array containing indices of heel-strikes.

    Returns
    -------
    strides_list : list
        Each element of this list will contain an individal stride from the
        input signal. I.e., strides_list[0] will return an array for the the
        first stride. These are in a list because they don't have a uniform
        length. One stride might have a length of 1000 while another has a
        length of 1020, so they won't fit in a DataFrame yet.

    """

    # create an empty list that will contain arrays of data for individual
    # strides
    strides_list = []

    # loop through indices and chop out individual strides. Start a counter to
    # keep track of which index we are chopping from.
    old_index = 0
    for index in heel_strike_indices:

        # get the stride using the indices to chop it out of the signal
        stride = signal[old_index:index]

        # append the stride array to the list
        strides_list.append(stride)

        # increment the old index
        old_index = index

    # first step is not valid because the first loop chopped from 0:idx, and
    # 0 was almost definitely not a heel strike
    strides_list.pop(0)

    return strides_list

# %% trial_strides

def trial_strides(phase, trial):
    """
    Given a single trial full of signals/measurements and the real-time gait
    phase estimate, return a dictionary full of signals chopped into strides
    of non-uniform vector length.
    
    This function uses the phase signal to compute heel-strike indices and then
    calls "get_stride_list" over each signal in the trial.

    Parameters
    ----------
    phase : ndarray
        This is the real-time phase estimate signal from the knee exoskeleton.
    trial : DataFrame
        A dataframe containing multiple signals from the exoskeleton over the
        course of a single ten-second data collection.

    Returns
    -------
    strides : dictionary
        A dictionary where keys are signal names and values are Python lists of
        strides. Each element of the list is an ndarray of variable length.

    """
    
    # 'where' command returns heel-strike indices
    heel_strike_indices = np.where(phase==0)[0]

    # sometimes due to a weird bug, the program thinks the very last data point
    # is a heel strike. That is virtually never the case, so we'll check if
    # the last point is a heel strike and drop it if so.
    if heel_strike_indices[-1] == len(phase)-1:
        heel_strike_indices = heel_strike_indices[0:-1]

    # get a list of strides for each signal and store inside of a dictionary
    strides = {}
    for signal_name in trial:
        
        # extract signal
        signal = trial[signal_name].values
        
        # get the stride list and add it to the dictionary
        strides[signal_name] = get_stride_list(signal, heel_strike_indices)

    return strides

# %% normalize_trial_strides

def normalize_trial_strides(strides):
    """
    This function takes variable-length strides and normalizes them in time to 
    a uniform length of 500 elements using linear interpolation. The function
    operates on a single trial.

    Parameters
    ----------
    strides : dictionary
        A dictionary where keys are signal names and values are Python lists of
        strides. Each element of the list is an ndarray of variable length.
        This is the output of the "trial_strides" function, and contains data
        from one trial only.

    Returns
    -------
    normalized_strides : dictionary
        Keys are signal names and values are ndarrays where each column is a
        single stride and rows represent increasing gait phase. Rows are
        normalized to a length of 500.
                                                                
    """

    # loop over each signal. preallocate a dictionary to be returned where
    # keys are signal names and values are multi-dimensional data arrays.
    normalized_strides = {}
    for signal in strides:
        
        # extract the list of variable-length strides for this signal
        strides_list = strides[signal]
        
        # create a list that will temporarily hold the normalized strides
        norm_stride = []

        # loop over each variable-length stride and create a corresponding
        # uniform-length stride.
        for stride_long in strides_list:

            # create an 'x' array that ranges from 0 to 100 and is the length
            # of this stride
            percent_gait_long = np.linspace(0, 100, len(stride_long))

            # create a 'x' array that is ranges from 0 to 100 and is length 500
            percent_gait_short = np.linspace(0, 100, 500)

            # interpolate a new stride at at the shortened domain. I.e., get
            # use the x-axis (percent_gait_long) and the y-axis (stride_long)
            # as lookup table with linear interpolation to get values for the
            # new shortened x-axis.
            stride_short = np.interp(x=percent_gait_short,
                                     xp=percent_gait_long,
                                     fp=stride_long)

            # append the normalized (short) stride to th list
            norm_stride.append(stride_short)

        # turn lists into array where each column is a step
        norm_stride = np.array(norm_stride).transpose()
        
        # put in dictionary to be returned                
        normalized_strides[signal] = norm_stride

    return normalized_strides

# %% package_strides

def package_strides(strides_filtered_norm, strides_raw_norm):
    """
    All filtered signals get normalized, but only one raw signal (phase) gets
    normalized. This function takes the output of "normalize_trial_strides"
    for the filtered and raw data and returns a single dictionary where
    signal names map to Pandas DataFrames where each column is a labeled, 
    uniform-length stride.
    
    This function is necessary because the "normalize_trial_strides" function
    is called by the primary gait pipeline twice, once for filtered signals and
    once for unfiltered signals in each trial. Here, we're just combining those
    results in a nice format.

    Parameters
    ----------
    strides_filtered_norm : dictionary
        Keys are signal names and values are ndarrays where each column is a
        single stride and rows represent increasing gait phase. Rows are
        normalized to a length of 500. This is the ouput of the
        "normalize_trial_strides" when called on a "filtered" dataframe
    strides_raw_norm : dictionary
        Keys are signal names and values are ndarrays where each column is a
        single stride and rows represent increasing gait phase. Rows are
        normalized to a length of 500. This is the ouput of the
        "normalize_trial_strides" when called on a "raw" dataframe

    Returns
    -------
    signals_dict : dictionary
        Keys are signal names and values are Pandas DataFrames where each
        column is a labeled, uniform-length stride.

    """

    # first see how many strides are in each signal by looking at GRFz
    grfz_array = strides_filtered_norm['GRFz (N)']
    num_strides = grfz_array.shape[1]

    # create a list of strings for column header names,
    # (i.e. Stride 0, ..., Stride N)
    column_names = []
    for i in range(num_strides):
        column_names.append('Stride '+str(i))
        
    # preallocate output dictionary
    signals_dict = {}
    
    # step one: convert all signals in 'filtered_norm' to DataFrames. Loop over
    # each signal in the dictionary
    for signal_name in strides_filtered_norm:

        # get a 500 row by N column numpy array containing strides for this
        # signal
        strides_array = strides_filtered_norm[signal_name]

        # convert to dataframe with column names from above
        df = pd.DataFrame(data=strides_array, columns=column_names)

        # store in signals_dict
        signals_dict[signal_name] = df
        
    # step two: get the raw gait phase signal and add it to the dict
    strides_array = strides_raw_norm['Gait Phase (%)']
    df = pd.DataFrame(data=strides_array, columns=column_names)
    signals_dict['Gait Phase (%)'] = df

    return signals_dict

# %% segment all signals for all trials for all participants into normalized strides

def segment_strides(data):
    """
    This is the primary pipeline function that uses the other functions in this
    file to chop every signal in every trial in every participant into strides
    with a uniform-vector length.
    
    Things are a little messy here and should be refactored in future analyses.
    Specifically, we want to chop out the 'gait phase' signal and the 

    Parameters
    ----------
    data : dictionary
        This is the primary gait pipeline data structure that contains all raw
        data, filtered data, metadata, etc.

    Returns
    -------
    None. Strides are appended to the input data structure in-place.

    """

    # loop over each participant
    for participant in data:
        
        # extract this participant's data and corresponding file names
        participant_data = data[participant]
        file_names = participant_data['file names']

        # loop over each file for a given participant
        participant_strides = {}
        for file in file_names:

            # extract filtered signals, raw signals, and gait phase
            trial_filtered = participant_data['filtered signals'][file]
            trial_raw = participant_data['raw signals'][file]
            phase = trial_raw['Gait Phase (%)'].values

            # chop each signal from the trial up into strides
            strides_filtered = trial_strides(phase, trial_filtered)
            strides_raw = trial_strides(phase, trial_raw)

            # create uniform-length stride vectors to normalize strides in time 
            strides_filtered_norm = normalize_trial_strides(strides_filtered)
            strides_raw_norm = normalize_trial_strides(strides_raw)

            # package all relevant strides for this file into a dictionary with
            # signal names as keys and Pandas DataFrames as values
            signals_dict = package_strides(strides_filtered_norm,
                                           strides_raw_norm)

            # place into container
            participant_strides[file] = signals_dict

        participant_data['strides'] = participant_strides

    return None
