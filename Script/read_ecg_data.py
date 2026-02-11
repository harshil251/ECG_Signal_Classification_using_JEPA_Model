#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from biosppy import utils
import pandas as pd


def read_ecg(file,result):
    
    """ Preprocesses an ECG signal.

    Parameters
    ----------
    file : numpy.ndarray
        Raw ECG signal.
    result : numpy.ndarray
        Subject data extracted from the DataSet.csv file    
        
    Returns
    -------
    ID : numpy.ndarray 
    Age : numpy.ndarray 
    Weight:  numpy.ndarray 
    Height:numpy.ndarray 
    Gender:numpy.ndarray 
    Observations field:numpy.ndarray 
    A1 : numpy.ndarray 
        ECG signal extracted from sensor A1 (with flat electrode texture).
    A2 : numpy.ndarray 
        ECG signal extracted from sensor A2 (with sinusoidal electrode texture).   
    A3 : numpy.ndarray 
        ECG signal extracted from sensor A2 (with pyramidal electrode texture).
    A4 : numpy.ndarray 
        ECG signal extracted from sensor A4 (with trapezoidal electrode texture).
    """
    
    def convert_raw_mV(raw):
        sig=list(map(int,(raw)))     
        sig=np.subtract(1024, sig)
        sig=(np.divide(sig,1024.)-0.5)*(33/11)#Unit -mV
        return sig
    
    with open(file, "r") as f:
        aux = f.readlines()     

    signal = np.loadtxt(file)
    
    lista1=[str(x) for x in [int(x) for x in signal[:, 5]]] 
    A1=convert_raw_mV(lista1)
    lista2=[str(x) for x in [int(x) for x in signal[:, 6]]]
    A2=convert_raw_mV(lista2)
    lista3=[str(x) for x in [int(x) for x in signal[:, 7]]]
    A3=convert_raw_mV(lista3)
    lista4=[str(x) for x in [int(x) for x in signal[:, 8]]]
    A4=convert_raw_mV(lista4)

    args = (
        result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],A1,A2,A3,A4)
    names = (
        "ID",
        "Age",
        "Weight ",
        "Height",
        "Gender",
        "Observations_field",
        "A1",
        "A2",
        "A3",
        "A4"
    )
    return utils.ReturnTuple(args, names)

if __name__ == "__main__":

    data_ecg=[]
    folder='ECG_EXP'
    df = pd.read_csv('DataSet.csv', sep=';')
    
    ind_files=utils.walktree(r''+folder+'', r'\.txt$');
    
    for i in ind_files:
        
        result = df[df['ID'].astype(str) == (utils.fileparts(i)[1])].values
        data_ecg.append(read_ecg(i,result))
