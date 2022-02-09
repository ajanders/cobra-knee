# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 12:55:48 2022

@author: Anthony Anderson

This group of functions imports a few csv files containing knee moments for
transtibial amputees and controls while walking. The data comes from the
following paper:
    
"Evaluation of a Powered Ankle-Foot Prosthetic System During Walking" by Ferris
et al. in Archives of Physical Medicine and Rehabilitation, 2012.

The paper contains a plot of knee flexion/extension moments as a function of
the gait cycle. I digitized these plots using a screen shot and a tool from:
    
https://plotdigitizer.com/app. 

The spacing of these plots are uneven. The functions here load the data,
interpolate it over an even spacing grid, and store it in a dictionary for
analysis in a primary script.

"""

import numpy as np
import pandas as pd
import scipy.signal as sg

# %% Import Data

def import_csv_files():
    """
    Import csv files containing digitized knee moments and return as DataFrames
    
    For each file, knee flexion is negative by the paper authors' definition.
    Units are Nm/kg body mass.

    Returns
    -------
    raw_control : DataFrame
        Contains phase and knee moment data for the healthy control subjects.
    raw_esr : DataFrame
        Contains phase and knee moment data for the amputees walking on energy
        storage and return prosthetic feet.
    raw_biom : DataFrame
        Contains phase and knee moment data for the amputees walking on robotic
        Biom ankle.

    """
    
    # directory where digitized csv files are stored
    directory = "../data/Digitized Knee Moments/"
    
    # load data from control subject
    raw_control = pd.read_csv(directory+"control-digitized.csv")
    raw_control.rename(columns={'x': 'Phase (%)', ' y': 'Knee Moment (Nm)'},
                       inplace=True)
    
    # load data from subject with energy storage and return foot
    raw_esr = pd.read_csv(directory+"ESR-digitized.csv")
    raw_esr.rename(columns={'x': 'Phase (%)', ' y': 'Knee Moment (Nm)'},
                   inplace=True)
    
    # load data from subject with robotic biom foot
    raw_biom = pd.read_csv(directory+"biom-digitized.csv")
    raw_biom.rename(columns={'x': 'Phase (%)', ' y': 'Knee Moment (Nm)'},
                    inplace=True)
    
    return raw_control, raw_esr, raw_biom

# %% Interpolate data for even spacing

def even_spacing(raw_control, raw_esr, raw_biom):
    """
    This function resamples digitized knee moment data at even spacing
    
    Parameters
    -------
    raw_control : DataFrame
        Contains phase and knee moments for healthy control subjects. Uneven
        spacing between data points.
    raw_esr : DataFrame
        Contains phase and knee moments for amputees walking on ESR feet. 
        Uneven spacing between data points.
    raw_control : DataFrame
        Contains phase and knee moment for amputees walking on Biom. Uneven
        spacing between data points.
    

    Returns
    -------
    phase : array
        Array going from 0 to 100 with 1000 evenly spaced points. x-axis.
    control_even : array
        Evenly spaced knee moments from healthy controls.
    esr_even : array
       Evenly spaced knee moments from amputees walking on ESR feet.
    biom_even : array
        Evenly spaced knee moments from amputees walking on Biom foot.

    """
    
    # generate an array of evenly spaced phase points to act as a common
    # x-axis for the three data sets
    phase = np.linspace(0, 100, 1000)
    
    # interpolate each trial
    
    # extract data array from 'raw' and get a two column numpy array
    control_array = raw_control.values
    # interpolate at evenly spaced points
    control_even = np.interp(phase, control_array[:,0], control_array[:,1])
    
    # extract data array from 'raw' and get a two column numpy array
    esr_array = raw_esr.values
    # interpolate at evenly spaced points
    esr_even = np.interp(phase, esr_array[:,0], esr_array[:,1])
    
    # extract data array from 'raw' and get a two column numpy array
    biom_array = raw_biom.values
    # interpolate at evenly spaced points
    biom_even = np.interp(phase, biom_array[:,0], biom_array[:,1])
    
    return phase, control_even, esr_even, biom_even
    
# %% Smooth

def smooth_moments(control_even, esr_even, biom_even):
    """
    The knee moments have digitization error due to manual user input. This
    function appplies a light filter to smooth out error.

    Parameters
    ----------
    control_even : array
        Array containing healthy control knee moments with digitization error.
    esr_even : array
        Array containing amputee ESR knee moments with digitization error.
    biom_even : array
        Array containing amputee Biom knee moments with digitization error.

    Returns
    -------
    control : array
        Array containing healthy control knee moments without digitization
        error.
    esr : TYPE
        Array containing amputee ESR knee moments without digitization
        error.
    biom : TYPE
        Array containing amputee Biom knee moments without digitization error.


    """
      
    # create a butterworth filter. Wn tuned by hand to apply light smoothing.
    b, a = sg.butter(N=2, Wn=0.1)
    
    # use filter to smooth
    control = sg.filtfilt(b, a, control_even)
    esr = sg.filtfilt(b, a, esr_even)
    biom = sg.filtfilt(b, a, biom_even)
    
    return control, esr, biom


# %% Get all data

def load_and_process_ferris_moments():
    """
    Loads, resamples, and smooths knee moments digitized from Ferris et. al,
    2012, as a dictionary.
    
    This function flips sign convention so that the positive direction is
    flexion.

    Returns
    -------
    knee_moments : dict
        Keys are phase, control, esr, and biom. Each maps to an array. Moments
        are in units of Nm/kg body mass.

    """
    
    # get data
    raw_control, raw_esr, raw_biom = import_csv_files()
    
    # interpolate at even spacing
    phase, control_even, esr_even, biom_even = even_spacing(raw_control,
                                                            raw_esr,
                                                            raw_biom)
    
    # smooth data to remove digitization error
    control, esr, biom = smooth_moments(control_even, esr_even, biom_even)
    
    # build dictionary
    knee_moments = {'phase': phase, 'control': -control,
                    'esr': -esr, 'biom': -biom}
    
    return knee_moments
    

