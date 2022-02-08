# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 21:03:40 2021

@author: Anthony

This group of function definitions can be used to apply low-pass Butterworth
filters to experimental data.

"""

import numpy as np
import scipy.signal as sg
import pandas as pd

# %% butterworth trial

def apply_butterworth_filter(trial, filter_frequencies, sampling_frequency=1000):
    """
    Apply a low-pass Butterworth filter to select signals within a data trial.

    This function accepts a Pandas DataFrame containing prosthesis signals and
    a dictionary with signal names and filter cut-off frequencies, and returns
    a new Pandas DataFrame with low-pass filtered signals.

    Parameters
    ----------
    trial : Pandas DataFrame
        This should be a DataFrame of raw signals collected on the COBRA ankle
        prosthesis. Each column is a signal name.
    filter_frequencies : Dictionary
        This dictionary contains the instructions for which signals to filter
        and at what frequency. Each key should be a string that matches one of
        the signal names in the DataFrame and each key should the desired
        cut-off frequency for that signal in Hz.

    Returns
    -------
    trial_filtered_signals : Pandas DataFrame
        This DataFrame will contain the newly filtered signals.

    """

    # constants to define size of data to be produced
    num_signals = len(filter_frequencies)
    trial_length_seconds = 10
    num_datapoints = trial_length_seconds*sampling_frequency

    # create an empty pandas dataframe to hold filtered signals for this trial
    empty_container = np.zeros((num_datapoints, num_signals))
    trial_filtered_signals = pd.DataFrame(data=empty_container,
                                          columns=filter_frequencies.keys())

    # iterate over each signal and filter
    for signal_name in filter_frequencies:

        # setup low-pass filter
        order = 2
        cutoff = filter_frequencies[signal_name]

        # extract the signal
        signal = trial[signal_name]

        # low pass filter
        b, a = sg.butter(N=order, Wn=cutoff/(0.5*sampling_frequency))
        filtered_signal = sg.filtfilt(b, a, signal)

        # put into container
        trial_filtered_signals[signal_name] = filtered_signal

    return trial_filtered_signals

# %%

def filter_participant_trials(trials, filter_frequencies):
    """
    Low-pass filter all trials for a single participant.

    Parameters
    ----------
    trials : Dictionary
        This parameter is a dictionary where each key is a file name and each
        value is a Pandas DataFrame of raw signals collected from the ankle
        prosthesis.
    filter_frequencies : Dictionary
        This dictionary contains the instructions for which signals to filter
        and at what frequency. Each key should be a string that matches one of
        the signal names in the DataFrame and each key should the desired
        cut-off frequency for that signal in Hz.

    Returns
    -------
    filtered_trials : Dictionary
        This output is a dictionary where each key is a file name and each
        value is a Pandas DataFrame of the newly filtered prosthesis signals.

    """

    # create a container for the filtered trials
    filtered_trials = {}

    # loop through all trials, filter each signal, and add it to the filtered
    # trials dict
    for name in trials:

        # extract a single trial
        trial = trials[name]

        # filter the select signals in that trial
        filtered_signals = apply_butterworth_filter(trial, filter_frequencies)

        # add to dict to return
        filtered_trials[name] = filtered_signals

    return filtered_trials


# %% filter signals

def filter_signals(data, filter_frequencies):
    """
    Zero-lag low-pass filter different signals at unique cutoff frequencies for
    all participants and all trials.

    This function uses a bi-directional low-pass Butterworth filter. Nothing is
    returned because the input data structure is modified in place.

    Parameters
    ----------
    filter_frequencies : dict
        Each key is a signal present in the real-time data. Each value is a
        the cutoff frequency at which to low pass filter than signal.

    Returns
    -------
    None.

    """

    # iterate over each participant
    for participant in data:

        # extract raw data for all trials
        trials = data[participant]['raw signals']

        # filter select signals from each trial and get as dict
        filtered_trials = filter_participant_trials(trials, filter_frequencies)

        # put the data in the primary data structure
        data[participant]['filtered signals'] = filtered_trials

    return None