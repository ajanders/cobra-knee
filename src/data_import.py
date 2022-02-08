# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 17:22:33 2021

@author: Anthony Anderson

This group of functions imports data stored in LabVIEW binary TDMS files and
stores them in a large data structure. The highest-level function is called
import_multiple_participant_data(). When called from a data analysis script,
it will call the other functions to import experimental data.

"""

import numpy as np
import pandas as pd
import glob
from nptdms import TdmsFile
import os

# %% tdms_to_DataFrame

def tdms_to_dataframe(file_name):
    """
    Load a LabVIEW binary TDMS file and return as a Pandas DataFrame.

    Parameters
    ----------
    fileName : string
        This string should be the file name of a tdms file that is to be
        loaded. If the file name is "stiffness01.tdms", input "stiffness01".
        If the files are in a different directory, include the full path in
        the file name.

    Returns
    -------
    data : DataFrame
        Each column is a signal recorded in real-time.

    """

    # load the tdms file
    path = file_name + '.tdms'
    tdms_file = TdmsFile.read(path)

    # iterate over groups/channels of tdms file and append to list
    tempList = []
    for group in tdms_file.groups():
        for channel in group.channels():
            channel_name = channel.name
            data = channel[:]
            d = {channel_name: data}
            tempList.append(pd.DataFrame(data=d))

    # convert data to dataframe
    data_frame = pd.concat(tempList, axis=1)

    # add an time column
    sampFreqHz = 1000
    time = np.arange(0, len(data)/sampFreqHz, 1/sampFreqHz)
    data_frame['Time'] = time

    return data_frame

# %% import all trials

def import_trials(directory):
    """
    Import all LabVIEW tdms files in a directory as Pandas dataframes.

    Parameters
    ----------
    directory : string
        Directory with a bunch of .tdms files to be imported.

    Returns
    -------
    trials : dict
        This dictionary has file names as keys and pandas DataFrames as
        values. The DataFrames contain the contents of a 10-second trial of
        time series signals collected from the treadmill and prosthesis
        sensors.
    trials_metadata : dict
        This dictionary has file names as keys and pandas DataFrames as
        values. The DataFrames contain the static parameters for the prosthesis
        control system.

    """

    # get a list of tdms files in the specified directory
    files = glob.glob(directory+'*.tdms')

    # get a list of file names with full path that are not metadata files
    data_files = []
    for file in files:
        if 'metadata' not in file:
            data_files.append(file)

    # make a dict, where the key is the file name and the value is another
    # dict. second level dict will have keys for 'data' and 'metadata' where
    # each value is a pandas DataFrame

    # initialize empy dictionary and empty list to contain file names
    trials = {}
    trials_metadata = {}
    file_names = []
    for file in data_files:
        # get the file and metadata file names as strings without the .tdms
        # extension
        file_name = file.replace('.tdms', '')
        metadata_file_name = file_name+'_metadata'

        # import tdms file as dataframe
        trial_data = tdms_to_dataframe(file_name)

        # check to see if associated metadata file exists and import
        if os.path.exists(metadata_file_name+'.tdms'):
            trial_metadata = tdms_to_dataframe(metadata_file_name)
        else:
            # assign empty list if not
            trial_metadata = []

        # create a key for the experiment using the file name without the
        # directory
        file_no_path = file_name.replace(directory, '')

        # assign trial and trial metadata to dicts, and file names to list
        trials[file_no_path] = trial_data
        trials_metadata[file_no_path] = trial_metadata
        file_names.append(file_no_path)

    return trials, trials_metadata, file_names

# %% load data from multiple participants

def import_multiple_participant_data(participants):
    """
    Return a data structure than contains data from one or more participants

    Parameters
    ----------
    participants : list
        List of strings that list participant names to import. This function
        assumes that there is a folder with the participant name in the data
        folder of the main directory.

    Returns
    -------
    data : dict
        Keys are participant names, values are dicts that hold data and
        metadata for all trials in the participant directory.

    """

    # build list of directories
    directories = []
    for participant in participants:
        directories.append('..\\data\\raw\\'+participant+'\\')

    # import trials from each directory
    data = {}
    for count, directory in enumerate(directories):

        # create an empty container for this participant
        participant_data = {}

        # import each trial in the directory
        trials, trials_metadata, file_names = import_trials(directory)

        # store raw trials in a dictionary
        participant_data['raw signals'] = trials
        participant_data['metadata'] = trials_metadata
        participant_data['file names'] = file_names

        # put that dictionary inside of dict that has participant names for
        # keys
        participant_name = participants[count]
        data[participant_name] = participant_data

    return data