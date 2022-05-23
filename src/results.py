# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:12:37 2022

@author: Anthony Anderson

This script computes the final quantitative outcomes that will be put in the
text and tables of the paper. These outcomes are:
    
    1. Peak exoskeleton torque and corresponding cable force.
    2. Mean and SD exoskeleton range of motion across all trials.
    3. Torque tracking RMS errors across all conditions. 

"""

import numpy as np

# %% compute peak torque across conditions

def compute_peak_torque_across_conditions(data):
    
    signals_conditions = data['BP A 010']['averages']['conditions']
    
    trans = signals_conditions['transparent']
    low = signals_conditions['low']
    med = signals_conditions['medium']
    high = signals_conditions['high']
    
    percent_gait = np.linspace(0, 100, len(trans['GRFz (N)']['Mean']))
    
    trans_mean = trans['Joint Torque (Nm)']['Mean']
    trans_sd = trans['Joint Torque (Nm)']['SD']
    trans_mean = trans_mean[percent_gait<70]
    trans_sd = trans_sd[percent_gait<70]
    peak_trans_mean = np.max(trans_mean)
    peak_trans_sd = trans_sd[np.where(trans_mean==peak_trans_mean)[0][0]]
    
    low_mean = low['Joint Torque (Nm)']['Mean']
    low_sd = low['Joint Torque (Nm)']['SD']
    low_mean = low_mean[percent_gait<70]
    trans_sd = low_sd[percent_gait<70]
    peak_low_mean = np.max(low_mean)
    peak_low_sd = low_sd[np.where(low_mean==peak_low_mean)[0][0]]
    
    med_mean = med['Joint Torque (Nm)']['Mean']
    med_sd = med['Joint Torque (Nm)']['SD']
    med_mean = med_mean[percent_gait<70]
    med_sd = med_sd[percent_gait<70]
    peak_med_mean = np.max(med_mean)
    peak_med_sd = med_sd[np.where(med_mean==peak_med_mean)[0][0]]
    
    high_mean = high['Joint Torque (Nm)']['Mean']
    high_sd = high['Joint Torque (Nm)']['SD']
    high_mean = high_mean[percent_gait<70]
    high_sd = high_sd[percent_gait<70]
    peak_high_mean = np.max(high_mean)
    peak_high_sd = high_sd[np.where(high_mean==peak_high_mean)[0][0]]
    
    peak_torques = {'transparent': (peak_trans_mean, peak_trans_sd),
                    'low': (peak_low_mean, peak_low_sd),
                    'med': (peak_med_mean, peak_med_sd),
                    'high': (peak_high_mean, peak_high_sd)}
    
    return peak_torques

# %% compute_maximum_torque_all_trials

def compute_maximum_torque_all_trials(data):
    """
    Find the highest torque provided by the exoskeleton during the experiment.

    Parameters
    ----------
    data : dictionary
        This is the primary data structure in the main gait processing
        pipeline, and contains all raw data, filtered data, segmented gait
        cycles, etc.

    Returns
    -------
    peak_torque : float
        The highest recorded torque applied by the exoskeleton.

    """
    
    # extract filtered signals. Participant identifier is hard-coded.
    filtered_signals = data['BP A 010']['filtered signals']
    
    # loop through files and find highest torque
    peak_torque = 0
    for file_name in filtered_signals:
        
        # extract torque signal
        torque = filtered_signals[file_name]['Joint Torque (Nm)'].values
        
        # compute max value
        trial_peak_torque = np.max(torque)
        
        # compare to pre-initialized peak torque and overwrite if greater
        if trial_peak_torque > peak_torque:
            peak_torque = trial_peak_torque
        
    return peak_torque

# %% compute mean and sd range of motion for a set of strides

def compute_trial_rom(strides):
    
    strides_angles = strides['Exoskeleton Angle (deg)']
    
    rom_list = []
    for stride_number in strides_angles:
        stride = strides_angles[stride_number]
        
        max_angle = np.max(stride)
        min_angle = np.min(stride)
        rom = max_angle - min_angle
        rom_list.append(rom)
        
    # convert rom list to array
    rom_array = np.array(rom_list)
    mean_rom = np.mean(rom_array)
    sd_rom = np.std(rom_array)
    
    return mean_rom, sd_rom

# %% compute RoM across conditions

def compute_RoM_across_conditions(data):
    
    # compute rom for transparent mode
    strides_0 = data['BP A 010']['strides']['transparent_0']
    strides_1 = data['BP A 010']['strides']['transparent_1']
    
    mean_rom_0, sd_rom_0 = compute_trial_rom(strides_0)
    mean_rom_1, sd_rom_1 = compute_trial_rom(strides_1)
    mean_rom_trans = (mean_rom_0 + mean_rom_1)/2
    sd_rom_trans = (sd_rom_0 + sd_rom_1)
    
    # compute rom for low mode
    strides_0 = data['BP A 010']['strides']['low_0']
    strides_1 = data['BP A 010']['strides']['low_1']
    
    mean_rom_0, sd_rom_0 = compute_trial_rom(strides_0)
    mean_rom_1, sd_rom_1 = compute_trial_rom(strides_1)
    mean_rom_low = (mean_rom_0 + mean_rom_1)/2
    sd_rom_low = (sd_rom_0 + sd_rom_1)/2
    
    # compute rom for medium mode
    strides_0 = data['BP A 010']['strides']['med_0']
    strides_1 = data['BP A 010']['strides']['med_1']
    
    mean_rom_0, sd_rom_0 = compute_trial_rom(strides_0)
    mean_rom_1, sd_rom_1 = compute_trial_rom(strides_1)
    mean_rom_med = (mean_rom_0 + mean_rom_1)/2
    sd_rom_med = (sd_rom_0 + sd_rom_1)/2
        
    # compute rom for high mode
    strides_0 = data['BP A 010']['strides']['high_0']
    strides_1 = data['BP A 010']['strides']['high_1']
    
    mean_rom_0, sd_rom_0 = compute_trial_rom(strides_0)
    mean_rom_1, sd_rom_1 = compute_trial_rom(strides_1)
    mean_rom_high = (mean_rom_0 + mean_rom_1)/2
    sd_rom_high = (sd_rom_0 + sd_rom_1)/2
    
    rom_conditions = {'transparent': (mean_rom_trans, sd_rom_trans),
                      'low': (mean_rom_low, sd_rom_low),
                      'medium': (mean_rom_med, sd_rom_med),
                      'high': (mean_rom_high, sd_rom_high)}
    
    return rom_conditions

# %%

def compute_tracking_error_two_files(data, file_0, file_1):
    
    # extract filtered signals
    filtered_signals = data['BP A 010']['filtered signals']
    
    signal = 'Joint Torque Setpoint (Nm)'
    setpoint_0 = filtered_signals[file_0][signal].values
    setpoint_1 = filtered_signals[file_1][signal].values
    setpoint = np.concatenate((setpoint_0, setpoint_1))
    
    signal = 'Joint Torque (Nm)'
    torque_0 = filtered_signals[file_0][signal].values
    torque_1 = filtered_signals[file_1][signal].values
    torque = np.concatenate((torque_0, torque_1))
    
    
    error = setpoint-torque
    rmse = np.sqrt(np.mean(error**2))
    
    return rmse

# %% compute_tracking_error

def compute_tracking_error_across_conditions(data):
    """
    This function computes the root mean squared (RMS) torque tracking error
    across all trials and then merges trials to compute errors across
    conditions.

    Parameters
    ----------
    data : dictionary
        This is the primary data structure in the main gait processing
        pipeline, and contains all raw data, filtered data, segmented gait
        cycles, etc.

    Returns
    -------
    tracking_errors : dictionary
        Keys are conditions (transparent, low, medium, high), keys are rms
        tracking error values.

    """    
    
    
    file_0 = 'transparent_0'
    file_1 = 'transparent_1'
    trans_rmse = compute_tracking_error_two_files(data, file_0, file_1)
    
    file_0 = 'low_0'
    file_1 = 'low_1'
    low_rmse = compute_tracking_error_two_files(data, file_0, file_1)
    
    file_0 = 'med_0'
    file_1 = 'med_1'
    med_rmse = compute_tracking_error_two_files(data, file_0, file_1)
    
    file_0 = 'high_0'
    file_1 = 'high_1'
    high_rmse = compute_tracking_error_two_files(data, file_0, file_1)
    
    
    # add to dictionary for storage
    tracking_errors = {'transparent': trans_rmse,
                       'low': low_rmse,
                       'med': med_rmse,
                       'high': high_rmse}
    
    
    return tracking_errors

# %%

def compute_outcomes(data):
    """
    This function computes all of the quantitative outcomes that make it into
    the paper. Data is added to a 'outcomes' section of the primary data
    structure.

    Parameters
    ----------
    data : dictionary
        This is the primary data structure in the main gait processing
        pipeline, and contains all raw data, filtered data, segmented gait
        cycles, etc.

    Returns
    -------
    None. Results dictionary is added to the primary data structure. Can be
    accessed with 'outcomes' key.

    """
    
    # get the peak +/- sd stance phase torque for each condition
    peak_torques = compute_peak_torque_across_conditions(data)
    
    # get the peak torques and cable forces, each returned as scalars
    max_torque = compute_maximum_torque_all_trials(data)
    max_force = max_torque/0.055
    
    # get the mean and standard deviation range of motion of the exoskeleton
    # as floats
    rom_outcomes = compute_RoM_across_conditions(data)
    
    # get the RMS tracking errors for all trials as a dictionary
    tracking_errors = compute_tracking_error_across_conditions(data)
    
    # package everything in a dictionary
    outcomes = {'peak torques': peak_torques,
                'max torque': max_torque,
                'max force': max_force,
                'rom across conditions': rom_outcomes,
                'tracking errors': tracking_errors}
    
    data['BP A 010']['outcomes'] = outcomes
    
    return None