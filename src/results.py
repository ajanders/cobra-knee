# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:12:37 2022

@author: Anthony Anderson

This script computes the final quantitative outcomes that will be put in the
text and tables of the paper.

"""

import numpy as np

# %% peak torques

def compute_peak_torque_all_trials(data):
    """
    Find the highest torque provided by the exoskeleton during the experiment.

    Parameters
    ----------
    data : dictionary
        DESCRIPTION.

    Returns
    -------
    peak_torque : TYPE
        DESCRIPTION.

    """
    
    # extract filtered signals
    filtered_signals = data['BP A 010']['filtered signals']
    
    # loop through files and find highest torque
    peak_torque = 0
    for file_name in filtered_signals:
        
        # extract torque signal
        torque = filtered_signals[file_name]['Joint Torque (Nm)'].values
        
        # compute max
        trial_peak_torque = np.max(torque)
        
        # compare to pre-initialized peak torque and overwrite if greater
        if trial_peak_torque > peak_torque:
            peak_torque = trial_peak_torque
        
    return peak_torque

# %% rom

def compute_RoM_all_trials(data):
    
    # extract filtered signals
    filtered_signals = data['BP A 010']['filtered signals']
    
    # loop through files and find highest torque
    max_angle = 0
    min_angle = 0
    for file_name in filtered_signals:
        
        # extract encoder signal
        angle = filtered_signals[file_name]['Exoskeleton Angle (deg)'].values
        
        # center the encoder signal by subtracting the mean to account for
        # angle changes caused by adjusting straps between trials.
        angle = angle - np.mean(angle)
        
        # compute max and min
        trial_max_angle = np.max(angle)
        trial_min_angle = np.min(angle)
        
        # compare to pre-initialized peak angles and overwrite if higher/lower
        if trial_max_angle > max_angle:
            max_angle = trial_max_angle
            
        if trial_min_angle < min_angle:
            min_angle = trial_min_angle
            
    # subtract the min from the max to get range of motion
    range_of_motion = max_angle - min_angle
        
    return range_of_motion

# %%

def compute_tracking_error_all_trials(data):
    
    # extract filtered signals
    filtered_signals = data['BP A 010']['filtered signals']
    
    # loop over each file and compute error
    tracking_errors = {}
    for file in filtered_signals:
        
        setpoint = filtered_signals[file]['Joint Torque Setpoint (Nm)']
        torque = filtered_signals[file]['Joint Torque (Nm)']
        error = setpoint-torque
        
        rmse = np.sqrt(np.mean(error**2))
        
        tracking_errors[file] = rmse
    
    return tracking_errors

# %%

def compute_outcomes(data):
    
    # get the peak torques and cable forces, each returned as scalars
    peak_torque = compute_peak_torque_all_trials(data)
    peak_force = peak_torque/0.055
    
    # get the range of motion of the exoskeleton as a scalar
    range_of_motion = compute_RoM_all_trials(data)
    
    # get the RMS tracking errors for all trials as a dictionary
    tracking_errors = compute_tracking_error_all_trials(data)
    
    # package everything in a dictionary
    outcomes = {'peak torque': peak_torque,
                'peak force': peak_force,
                'range of motion': range_of_motion,
                'tracking errors': tracking_errors}
    
    data['BP A 010']['outcomes'] = outcomes
    
    return None