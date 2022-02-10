# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:12:58 2022

@author: Anthony Anderson

I forgot to zero the treadmills before our data collection, so they have a
weird offset in them. This function will zero the vertical GRFs for analysis
of the pilot data. Won't forget to zero for the real data collection.

"""

import numpy as np

# %%

def zero_grf(grf_z):
    """
    Remove static offset in GRF by making the minimum value "zero".

    Parameters
    ----------
    grf_z : ndarray
        Ground reaction force with offset.

    Returns
    -------
    grf_z : ndarray
        Ground reaction force without offset.

    """

    min_grf = np.min(grf_z)
    grf_z = grf_z - min_grf

    return grf_z

# %%

def zero_all_grfs(data):
    """
    Iterate over all files for all participants and remove the offset from all
    ground reaction forces.

    Parameters
    ----------
    data : dict
        big dictionary containing all experimental data.

    Returns
    -------
    None.

    """

    # iterate over every participant
    for participant in data:

        # get the structure containing raw signals for all files
        raw_signals = data[participant]['raw signals']

        # iterate over each file
        for file in raw_signals:

            # extract grf
            grf_z = raw_signals[file]['GRFz (N)'].values

            # zero
            grf_z = zero_grf(grf_z)

            # put back in container
            raw_signals[file]['GRFz (N)'] = grf_z

    return None