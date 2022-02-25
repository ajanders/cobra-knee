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

# %% compute_peak_torque_all_trials

def compute_peak_torque_all_trials(data):
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

# %% compute_RoM_all_trials

def compute_RoM_all_trials(data):
    """
    Compute the average range of motion of the exoskeleton over all trials.
    Exclude trials where the exoskeleton was not worn.

    Parameters
    ----------
    data : dictionary
        This is the primary data structure in the main gait processing
        pipeline, and contains all raw data, filtered data, segmented gait
        cycles, etc.

    Returns
    -------
    range_of_motion : float
        The average encoder range of motion over all trials

    """
    
    # extract filtered signals
    signals = data['BP A 010']['filtered signals']
    
    # list of files to ignore because exo was not on the person
    excluded_files = ['no_exo_0', 'no_exo_1', 'no_exo_2']
    
    # range of motion list
    rom_list = []
    
    # loop through files and compute range of motion for each
    for file_name in signals:
        
        if file_name not in excluded_files:
        
            # extract encoder signal
            angle = signals[file_name]['Exoskeleton Angle (deg)'].values
                      
            # compute max and min
            trial_max_angle = np.max(angle)
            trial_min_angle = np.min(angle)
            
            # compute range of motion
            rom = trial_max_angle - trial_min_angle
            
            # append rom for this trial to the list
            rom_list.append(rom)
            
    # compute mean and standard deviations
    mean_rom = np.mean(np.array(rom_list))
    sd_rom = np.std(np.array(rom_list))
        
    return mean_rom, sd_rom

# %% compute_tracking_error

def compute_tracking_error(data):
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
    
    # extract filtered signals
    filtered_signals = data['BP A 010']['filtered signals']
    
    # loop over each file and compute error
    errors = {}
    for file in filtered_signals:
        
        setpoint = filtered_signals[file]['Joint Torque Setpoint (Nm)']
        torque = filtered_signals[file]['Joint Torque (Nm)']
        error = setpoint-torque
        
        rmse = np.sqrt(np.mean(error**2))
        
        errors[file] = rmse
        
    # uses individual files to compute errors accross conditions
    transparent_rms = (errors['transparent_0'] + errors['transparent_1'])/2
    low_rms = (errors['low_0'] + errors['low_1'])/2
    med_rms = (errors['med_0'] + errors['med_1'])/2
    high_rms = (errors['high_0'] + errors['high_1'])/2
    total_rms = (transparent_rms + low_rms + med_rms + high_rms)/4
        
    # add to dictionary for storage
    tracking_errors = {'transparent': transparent_rms,
                       'low': low_rms,
                       'med': med_rms,
                       'high': high_rms,
                       'total': total_rms}
    
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
    # get the peak torques and cable forces, each returned as scalars
    peak_torque = compute_peak_torque_all_trials(data)
    peak_force = peak_torque/0.055
    
    # get the mean and standard deviation range of motion of the exoskeleton
    # as floats
    mean_rom, sd_rom = compute_RoM_all_trials(data)
    
    # get the RMS tracking errors for all trials as a dictionary
    tracking_errors = compute_tracking_error(data)
    
    # package everything in a dictionary
    outcomes = {'peak torque': peak_torque,
                'peak force': peak_force,
                'average range of motion': mean_rom,
                'sd range of motion': sd_rom,
                'tracking errors': tracking_errors}
    
    data['BP A 010']['outcomes'] = outcomes
    
    return None