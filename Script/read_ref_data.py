#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmltodict
from biosppy import utils

def read_ref(file,id_file):
    
    """ Preprocesses an ECG REF signal.

    Parameters
    ----------
    file : array
        Raw ECG signal.
    
    Returns
    -------
    acquisitionDateTime : numpy.ndarray
        The date and time of the acquisition.
    name_dev : numpy.ndarray
        The identification of each lead acquired (e.g. I, II, III, AVR, AVL, AVF, V1, V2, V3, V4, V5, V6).
    meanTemplate : numpy.ndarray
        Average of the heartbeat models extracted for each lead.
    dev : numpy.ndarray
        Time series signal extracted for each lead over a period of 10s.
    unit : Unit of the extracted signal (uV).
    """

    name_dev=[]
    meanTemplate=[]
    dev=[]
    with open(file,"r") as xml_obj:
        
        obj = xmltodict.parse(xml_obj.read())
        xml_obj.close()
        
    acquisitionDateTime=list(obj['sapphire']['dcarRecord']['patientInfo']['visit']['order']['testInfo']['acquisitionDateTime'].values())
    aux=obj['sapphire']['dcarRecord']['patientInfo']['visit']['order']['ecgResting']['params']['ecg']
    auxT=aux['var']['medianTemplate']['ecgWaveformMXG']['ecgWaveform']
    auxD=aux['wav']['ecgWaveformMXG']['ecgWaveform']
    
    for x in range(0,12):
        
        name_dev.append(list(auxT[x].values())[0])   
        aux_=list(auxT[x].values())[4].split(' ')
        meanTemplate.append(list(map(float,aux_)))
        aux_=list(auxD[x].values())[4].split(' ')
        dev.append(list(map(float,aux_)))
        
    unit='uV'
        
    args = (
        id_file,acquisitionDateTime, name_dev, meanTemplate, dev, unit)
    names = (
        "id",
        "acquisitionDateTime",
        "name_dev",
        "meanTemplate",
        "dev",
        "unit"
    )


    return utils.ReturnTuple(args, names)

if __name__ == "__main__":
    
    data_ref=[]
    folder='ECG_REF'
    ind_files=utils.walktree(r''+folder+'', r'\.XML$');
    for i in ind_files:
        
        data_ref.append(read_ref(folder+'/'+utils.fileparts(i)[1]+'.XML',utils.fileparts(i)[1]))
    


