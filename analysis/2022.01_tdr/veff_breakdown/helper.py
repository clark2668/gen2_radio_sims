import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
import os
import sys
import pickle
from multiprocessing import Pool
from NuRadioReco.utilities import units
from NuRadioMC.utilities.Veff import get_Veff_water_equivalent as gwe

def tmp(filename, hybrid_list, shallow_list, hybrid_trigger, shallow_trigger):
    print("Filename {}".format(filename))

    fin = h5py.File(filename, "r")
    summary = {}
    summary['n_events'] = fin.attrs['n_events']
    summary['volume'] = fin.attrs['volume']
    summary['czmin'] = np.cos(fin.attrs['thetamax'])
    summary['czmax'] = np.cos(fin.attrs['thetamin'])
    summary['thetamin'] = fin.attrs['thetamin']
    summary['thetamax'] = fin.attrs['thetamax']
    summary['tot_weight'] = 0 

    # our goal is to figure out
    # first, how many events triggered in either the deep or the surface array
    # second, how many events triggered in just the deep array, just the surface array, or both
    # so, we will make a dictionary  of information
    # for every event (key), we will store an array (values)
    # the array will contain a weight
    # if it triggers at all
    # if it triggers deep, triggers shallow, or triggers both
    event_information = {}

    # get group ids of events that triggered
    ugids, uindex = np.unique(np.array(fin['event_group_ids']), 
        return_index=True)
    weights = np.array(fin['weights'])[uindex]
    weights_dict = {A:B for A,B in zip(ugids, weights)}
    try:
        tnames = fin.attrs['trigger_names']
    except:
        return None

    # tnames should be:
    # 0 = 'LPDA_2of4_100Hz'
    # 1 = 'LPDA_2of4_10mHz'
    # 2 = 'PA_8channel_100Hz'
    # 3 = 'PA_4channel_100Hz'
    # 4 = 'PA_8channel_1mHz'
    # 5 = 'PA_4channel_1mHz'
    # we want 0 and 3

    tname_to_index = {}
    for i, key in enumerate(tnames):
        tname_to_index[key] = i
    
    if hybrid_trigger not in tname_to_index:
        raise KeyError(f'Hybrid trigger ({hybrid_trigger}) is not in the hdf5 file list ({tnames})')
    if shallow_trigger not in tname_to_index:
        raise KeyError(f'Shallow trigger ({shallow_trigger}) is not in the hdf5 file list ({tnames})')


    # first, the hybrid-only part
    for key in fin.keys():
        if(key.startswith("station")):
            deep_id = int(key.split('_')[1])
            if deep_id not in hybrid_list:
                continue
            s_deep = fin[key]
            if 'multiple_triggers_per_event' in s_deep:
                triggers_deep = s_deep['multiple_triggers_per_event'][:, tname_to_index[hybrid_trigger]]
                evs_triggers_deep = np.unique(np.array(s_deep['event_group_ids'])[triggers_deep])
                
                for ev in evs_triggers_deep:
                    if ev not in event_information:
                        event_information[ev] = [weights_dict[ev], 0, 0]
                        event_information[ev][1] = 1 # seen in SOME hybrid station
                    elif ev in event_information:
                        event_information[ev][1] +=1 # increment the number of hybrid stations where this is seen

                
    # second, the shallow-only part
    for key in fin.keys():
        if(key.startswith("station")):
            shallow_id = int(key.split('_')[1])
            if shallow_id not in shallow_list:
                continue
            s_shallow = fin[key]
            if 'multiple_triggers_per_event' in s_shallow:
                triggers_shallow = s_shallow['multiple_triggers_per_event'][:, tname_to_index[shallow_trigger]]
                evs_triggers_shallow = np.unique(np.array(s_shallow['event_group_ids'])[triggers_shallow])
                
                for ev in evs_triggers_shallow:
                    if ev not in event_information:
                        event_information[ev] = [weights_dict[ev], 0, 0]
                        event_information[ev][2] = 1 # seen in SOME shallow station
                    elif ev in event_information:
                        event_information[ev][2] +=1 # increment the number of hybrid stations where this is seen

    tot_weight = 0
    hybrid_only_weight = 0
    shallow_only_weight = 0
    dual_weight = 0

    for ev in event_information:
        weight = event_information[ev][0]
        trig_hybr = event_information[ev][1]
        trig_shal = event_information[ev][2]

        num_trig_total = trig_hybr + trig_shal
        if num_trig_total > 0:
            tot_weight+=weight
        
        if trig_hybr and trig_shal:
            dual_weight+=weight
        elif trig_hybr and not trig_shal:
            hybrid_only_weight += weight
        elif trig_shal and not trig_hybr:
            shallow_only_weight += weight
        
    summary['tot_weight'] = tot_weight
    summary['hybrid_only_weight']  = hybrid_only_weight
    summary['shallow_only_weight'] = shallow_only_weight
    summary['dual_weight'] = dual_weight

    return summary
