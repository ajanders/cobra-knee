# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:11:59 2021

@author: Anthony
"""

import numpy as np
import pandas as pd

# %% detect heel strikes

def detect_heel_strike(grf, sampling_frequency=1000):
    """
    Given a filtered vertical ground reaction force, return a boolean array
    where True indicates that a heel strike occured at that instant.

    Heel strikes are detected using the derivative of the ground reaction
    force with respect to time. To avoid multiple peaks/valleys in the
    ground reaction force during mid-stance, the grf is 'saturated' at 25 N
    before the derivative is taken. This results in clean spikes in the rate
    as the foot contacts the ground.


    Parameters
    ----------
    grf : ndarray
        An array of vertical ground reaction forces in Newtons.

    Returns
    -------
    heel_strikes : ndarray
        An array of boolean values that are only True when a heel strike is
        detected.

    """

    # saturate the grf at 25 Newtons
    grf_saturated = grf*1

    # hacky temporary fix
    smallest_grf = np.min(grf_saturated)
    grf_saturated = grf_saturated - smallest_grf

    grf_saturated[grf_saturated>25] = 25

    # take derivative
    dt = 1/sampling_frequency
    grf_rate = np.gradient(grf_saturated, dt)

    # loop and detect heel strike
    over_thresh = np.zeros(len(grf_rate))
    heel_strikes = np.full(len(grf_rate), False)
    thrsh = 500
    for i in range(len(grf_rate)):

        # is the rate over the threshold?
        if grf_rate[i] > thrsh:
            over_thresh[i] = 1

        # is this the first time the signal has crossed the threshold for this
        # step?
        if (i>0) & (over_thresh[i]==1) & (over_thresh[i-1]==0):
            heel_strikes[i] = True

    return heel_strikes

# %% get heel strike indices

def get_heel_strike_indices(heel_strikes):
    """
    Given a boolean array where heel-strikes are True and everything else is
    False, return the indices of the heel-strikes.

    Parameters
    ----------
    heel_strikes : ndarray
        Boolean array where heel-strikes are true and everything else is False.

    Returns
    -------
    heel_strike_indices : ndarray
        A short array containing the indices of the heel-strikes.

    """

    # 'where' command returns indices
    heel_strike_indices = np.where(heel_strikes)[0]

    # sometimes due to a weird bug, the program thinks the very last data point
    # is a heel strike. That is virtually never the case, so we'll check if
    # the last point is a heel strike and drop it if so.
    if heel_strike_indices[-1] == len(heel_strikes)-1:
        heel_strike_indices = heel_strike_indices[0:-1]

    return heel_strike_indices

# %% get a list of stride arrays for a single signal

def get_stride_list(signal, heel_strike_indices):
    """
    Given a measurement (e.g. ground reaction force) and an array/list of
    heel-strike indices, chop out the individual strides from the signal and
    store them as arrays inside of a list.


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
        first stride.

    """

    # create an empty list that will contain arrays of data for individual
    # steps
    strides_list = []

    # loop through indices and chop out individual strides
    old_index = 0
    for index in heel_strike_indices:

        # get the foot step
        stride = signal[old_index:index]

        # append the array to the list
        strides_list.append(stride)

        # increment the old index
        old_index = index

    # first step is not valid because the first loop chopped from 0:idx, and
    # 0 was almost definitely not a heel strike
    strides_list.pop(0)

    return strides_list

# %% get strides from a trial

def trial_strides(heel_strike_indices, trial):
    """
    Given a single trial full of signals/measurements and an array/list of
    heel-strike indices,

    Parameters
    ----------
    heel_strike_indices : TYPE
        DESCRIPTION.
    trial : TYPE
        DESCRIPTION.

    Returns
    -------
    strides : TYPE
        DESCRIPTION.

    """

    # get a list of strides for each signal
    strides = {}
    for signal_name in trial:
        signal = trial[signal_name].values
        strides[signal_name] = get_stride_list(signal, heel_strike_indices)

    return strides

# %% normalize signals

def normalize_stride_list(strides_list):

    # normalize to time
    norm_stride = []

    # loop over un-normalized strides
    for stride_long in strides_list:

        # create a domain array that is the length of the stride
        percent_gait_long = np.linspace(0, 100, len(stride_long))

        # create a domain array that is length 500
        percent_gait_short = np.linspace(0, 100, 500)

        # interpolate a new stride at at the short domain
        stride_short = np.interp(percent_gait_short,
                                 percent_gait_long,
                                 stride_long)

        # append the normalized (short) stride to th list
        norm_stride.append(stride_short)

    # turn lists into array where each column is a step
    norm_stride = np.array(norm_stride).transpose()

    return norm_stride

# %% normalize trial strides

def normalize_trial_strides(strides):

    # input is a dict where signal names map to lists
    normalized_strides = {}
    for signal in strides:
        normalized_strides[signal] = normalize_stride_list(strides[signal])

    return normalized_strides

# %% package strides

def package_strides(strides_filtered_norm, strides_raw_norm):

    # inputs are dictionaries that map signal names to arrays

    # I want to combine the filtered and raw signals into a single dict
    # that maps signal name to Pandas DataFrame where each column is a stride

    # first get how many strides are in each signal by looking at GRFz
    grfz_array = strides_filtered_norm['GRFz (N)']
    num_strides = grfz_array.shape[1]

    # create a list for column header names (i.e. Stride 0, ..., Stride N)
    column_names = []
    for i in range(num_strides):
        column_names.append('Stride '+str(i))

    signals_dict = {}
    # step one: convert all signals in 'filtered_norm' to DataFrames
    for signal_name in strides_filtered_norm:

        strides_array = strides_filtered_norm[signal_name]

        # convert to dataframe
        df = pd.DataFrame(data=strides_array, columns=column_names)

        # store in signals_dict
        signals_dict[signal_name] = df

    return signals_dict

# %% get strides for a participant

def participant_strides(participant_data):

    file_names = participant_data['file names']

    participant_strides = {}
    for file in file_names:

        trial_filtered = participant_data['filtered signals'][file]
        trial_raw = participant_data['raw signals'][file]
        grf = trial_filtered['GRFz (N)'].values

        # first for this trial, I want to extract heel strikes
        heel_strikes = detect_heel_strike(grf)

        # then we need to get the indices needed to segment the gait cycle
        heel_strike_indices = get_heel_strike_indices(heel_strikes)

        # chop each signal from a trial up into strides
        strides_filtered = trial_strides(heel_strike_indices, trial_filtered)
        strides_raw = trial_strides(heel_strike_indices, trial_raw)

        # normalize strides to time
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

# %% strides for all participants

def strides(data):

    for participant in data:
        participant_strides(data[participant])

    return None
