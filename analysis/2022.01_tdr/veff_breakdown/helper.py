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
from NuRadioMC.utilities import cross_sections

def tmp(filename, hybrid_list, shallow_list, deep_trigger, shallow_trigger):
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
    
    if deep_trigger not in tname_to_index:
        raise KeyError(f'Hybrid trigger ({deep_trigger}) is not in the hdf5 file list ({tnames})')
    if shallow_trigger not in tname_to_index:
        raise KeyError(f'Shallow trigger ({shallow_trigger}) is not in the hdf5 file list ({tnames})')


    # first, the hybrid-only part
    for key in fin.keys():
        if(key.startswith("station")):
            hybrid_id = int(key.split('_')[1])
            if hybrid_id not in hybrid_list:
                continue
            s_hybrid = fin[key]
            if 'multiple_triggers_per_event' in s_hybrid:

                # this is the deep component of the hybrid array
                hybrid_triggers_deep = s_hybrid['multiple_triggers_per_event'][:, tname_to_index[deep_trigger]]
                evs_triggers_deep_hybrid = np.unique(np.array(s_hybrid['event_group_ids'])[hybrid_triggers_deep])
                
                for ev in evs_triggers_deep_hybrid:
                    if ev not in event_information:
                        event_information[ev] = [weights_dict[ev], 0, 0]
                        event_information[ev][1] = 1 # seen in SOME deep component
                    elif ev in event_information:
                        event_information[ev][1] +=1 # increment the number of deep components where this is seen

                # now the shallow component of the hybrid array
                hybrid_triggers_shallow = s_hybrid['multiple_triggers_per_event'][:, tname_to_index[shallow_trigger]]
                evs_triggers_shallow_hybrid = np.unique(np.array(s_hybrid['event_group_ids'])[hybrid_triggers_shallow])
                
                for ev in evs_triggers_shallow_hybrid:
                    if ev not in event_information:
                        event_information[ev] = [weights_dict[ev], 0, 0]
                        event_information[ev][2] = 1 # seen in SOME shallow component
                    elif ev in event_information:
                        event_information[ev][2] +=1 # increment the number of shallow components where this is seen

                
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
    deep_only_weight = 0
    shallow_only_weight = 0
    dual_weight = 0

    for ev in event_information:
        weight = event_information[ev][0]
        trig_deep = event_information[ev][1]
        trig_shal = event_information[ev][2]

        num_trig_total = trig_deep + trig_shal
        if num_trig_total > 0:
            tot_weight+=weight
        
        if trig_deep and trig_shal:
            dual_weight+=weight
        elif trig_deep and not trig_shal:
            deep_only_weight += weight
        elif trig_shal and not trig_deep:
            shallow_only_weight += weight
        
    summary['tot_weight'] = tot_weight
    summary['deep_only_weight']  = deep_only_weight
    summary['shallow_only_weight'] = shallow_only_weight
    summary['dual_weight'] = dual_weight

    return summary

def get_review_array():
    n_deep = 144*1
    n_shallow = (169+144)*1
    deep_det = 'pa_200m_2.00km'
    deep_trigger = 'PA_4channel_100Hz'
    shallow_det = 'surface_4LPDA_PA_15m_RNOG_300K_1.00km'
    shallow_trigger = 'LPDA_2of4_100Hz'

    flavors = ['e', 'mu', 'tau']
    energies = np.zeros(9)
    veffs = np.zeros((3,9))

    data_i = np.genfromtxt(f'results/review_array/tabulated_veff_aeff_review_hybrid.csv', delimiter=',', skip_header=6, names=['logE', 'dveff', 'daff', 'sveff', 'saeff', 'overlap_frac', 'deep_only', 'shallow_only'])
    energies = np.power(10.,data_i['logE'])
    average_total_veff = np.zeros(9)
    average_deep_veff = np.zeros(9)
    average_shallow_veff = np.zeros(9)
    average_dual_veff = np.zeros(9)
    average_total_aeff = np.zeros(9)
    average_deep_aeff = np.zeros(9)
    average_shallow_aeff = np.zeros(9)
    average_dual_aeff = np.zeros(9)

    for iF, flavor in enumerate(flavors):
        filename = f'results/review_array/overlap_{deep_det}_{deep_trigger}_{shallow_det}_{shallow_trigger}_{flavor}.pkl'
        data = pickle.load(open(filename, 'br'))
        for i, key in enumerate(data.keys()): # assume all have the same number of energies
            veff_total = data[key]['total_veff'] * 0.917  # convert to water equivalent
            veff_deep = data[key]['deep_only_veff'] * 0.917
            veff_shallow = data[key]['shallow_only_veff'] * 0.917
            veff_dual = data[key]['dual_veff'] * 0.917

            lint = cross_sections.get_interaction_length(np.power(10., float(key)))
            aeff_total = veff_total/lint
            aeff_deep = veff_deep/lint
            aeff_shallow = veff_shallow/lint
            aeff_dual = veff_dual/lint

            # convert to the right units (I could be more compact than this, but want to be explicit)
            veff_total = veff_total * 4 * np.pi / units.km**3
            veff_deep = veff_deep * 4 * np.pi / units.km**3
            veff_shallow = veff_shallow * 4 * np.pi / units.km**3
            veff_dual = veff_dual * 4 * np.pi / units.km**3

            aeff_total = aeff_total * 4 * np.pi / units.km**2
            aeff_deep = aeff_deep * 4 * np.pi / units.km**2
            aeff_shallow = aeff_shallow * 4 * np.pi / units.km**2
            aeff_dual = aeff_dual * 4 * np.pi / units.km**2

            average_total_veff[i] += veff_total
            average_deep_veff[i] += veff_deep
            average_shallow_veff[i] += veff_shallow
            average_dual_veff[i] += veff_dual

            average_total_aeff[i] += aeff_total
            average_deep_aeff[i] += aeff_deep
            average_shallow_aeff[i] += aeff_shallow
            average_dual_aeff[i] += aeff_dual

    # turn into flavor average
    average_total_veff/=3
    average_deep_veff/=3
    average_shallow_veff/=3
    average_dual_veff/=3
    average_total_aeff/=3
    average_deep_aeff/=3
    average_shallow_aeff/=3
    average_dual_aeff/=3

    return average_total_veff, average_deep_veff, \
            average_shallow_veff, average_dual_veff, \
            average_total_aeff, average_deep_aeff, \
            average_shallow_aeff, average_dual_aeff

