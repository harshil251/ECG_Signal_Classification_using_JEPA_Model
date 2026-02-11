#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import argrelextrema
from biosppy import utils
import read_ecg_data as red
import read_ref_data as rrd

def getAllPeaks(ecg_proc=None):
    
    t_position=getTPositions(ecg_proc)
    q_position=getQPositions(ecg_proc)
    s_position=getSPositions(ecg_proc)
    p_position=getPPositions(ecg_proc)

    rpeaks=ecg_proc['rpeaks']
    
    # output
    args = (p_position,q_position,rpeaks,s_position,t_position)
    names = (
        "ppeaks",
        "qpeaks",
        "rpeaks",
        "speaks",
        "tpeaks"
    )

    return utils.ReturnTuple(args, names)


def getQPositions(ecg_proc=None):
    """ 
    Parameters
    ----------
    signal : object
    object return by the function ecg.
    Returns
    -------
    Q_positions : array
            Array with all Q positions on the signal
    
    """

    template_r_position = 200  # R peek on the template is always on 100 index
    Q_positions = []

    for n, each in enumerate(ecg_proc["templates"]):
        # Get Q Position
        template_left = each[0 : template_r_position + 1]
        mininums_from_template_left = argrelextrema(template_left, np.less)
        # print("Q position= " + str(mininums_from_template_left[0][-1]))
        Q_position = ecg_proc["rpeaks"][n] - (
            template_r_position - mininums_from_template_left[0][-1]
        )
        Q_positions.append(Q_position)
       
    return Q_positions

def getSPositions(ecg_proc=None):
    """
    Parameters
    ----------
    signal : object
    object return by the function ecg.
    Returns
    -------
    S_positions : array
            Array with all S positions on the signal
   
    """

    template_r_position = 200  # R peek on the template is always on 100 index
    S_positions = []
    template_size = len(ecg_proc["templates"][0])

    for n, each in enumerate(ecg_proc["templates"]):
        # Get S Position
        template_right = each[template_r_position : template_size + 1]
        mininums_from_template_right = argrelextrema(template_right, np.less)
        S_position = ecg_proc["rpeaks"][n] + mininums_from_template_right[0][0]
        S_positions.append(S_position)

    return S_positions


def getPPositions(ecg_proc=None):
    """
    Parameters
    ----------
    signal : object
    object return by the function ecg.
    Returns
    -------
    P_positions : array
            Array with all P positions on the signal
   
    """

    template_r_position = 200  # R peek on the template is always on 100 index
    template_p_position_max = (
        80  # the P will be always hapenning on the first 80 indexes of the template
    )
    P_positions = []
   

    for n, each in enumerate(ecg_proc["templates"]):
        # Get P position
        template_left = each[0 : template_p_position_max + 1]
        max_from_template_left = np.argmax(template_left)
        # print("P Position=" + str(max_from_template_left))
        P_position = (
            ecg_proc["rpeaks"][n] - template_r_position + max_from_template_left
        )
        P_positions.append(P_position)

       
    return P_positions


def getTPositions(ecg_proc=None):
    """
    Parameters
    ----------
    signal : object
    object return by the function ecg.
    
    Returns
    -------
    T_positions : array
        Array with all T positions on the signal
    
    """

    template_r_position = 200  # R peek on the template is always on 100 index
    template_T_position_min = (
        270  # the T will be always hapenning after 150 indexes of the template
    )
    T_positions = []

    for n, each in enumerate(ecg_proc["templates"]):
        # Get T position
        template_right = each[template_T_position_min:]
        max_from_template_right = np.argmax(template_right)
        # print("T Position=" + str(template_T_position_min + max_from_template_right))
        T_position = (
            ecg_proc["rpeaks"][n]
            - template_r_position
            + template_T_position_min
            + max_from_template_right
        )
        T_positions.append(T_position)

    return T_positions


