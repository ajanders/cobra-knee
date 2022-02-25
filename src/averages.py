# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:28:23 2021

@author: Anthony
"""

import numpy as np
import pandas as pd

# %% all participants

def average_strides(data):

    # loop over each participant in the data set
    for participant in data:
        
        # extract data structure for this participant
        participant_data = data[participant]
        
        # extract the 'strides' data structure from the participant data
        # structure
        stride_data = participant_data['strides']

        # create a dictionary container for average strides for all files
        averages = {}

        # loop through each signal within each file and compute means and sd's
        for file_name in stride_data:

            # extract the time normalized strides for one file/trial
            trial = stride_data[file_name]

            # create a new data structure to hold average signals for this
            # trial
            file_averages = {}

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
                file_averages[signal_name] = df

            # once all signals have been iterated over, put the averages for
            # all signals in a dictionary where the file name is the key
            averages[file_name] = file_averages

        # after all files have been iterated over, store the complete output
        # under the key 'averages
        participant_data['averages'] = averages

    return None