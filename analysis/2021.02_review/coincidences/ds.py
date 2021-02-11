import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
from scipy import interpolate
import json
import os
import sys
import pickle
from radiotools import plthelpers as php
from multiprocessing import Pool
from NuRadioReco.utilities import units

n_cores = 10

path = "/project2/kicp/avieregg/gen2radio/output_500km2_03/run_output_500km2_04/surface_4LPDA_PA_15m_RNOG_300K_1.50km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/output/"
#path2 = "/project2/kicp/avieregg/gen2radio/output_500km2_03/run_output_500km2_04/surface_4LPDA_PA_15m_RNOG_300K_1.50km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/output/"
path2 = "/project2/kicp/avieregg/gen2radio/output_500km2_03/run_output_500km2_04/pa_100m_3.00km/config_Alv2009_noise_100ns/D05phased_array_deep/output/"
#path2 = "/project2/kicp/avieregg/gen2radio/output_500km2_03/run_output_500km2_04/pa_200m_3.00km/config_Alv2009_noise_100ns/D05phased_array_deep/output/"

#trigger_names = ['PA_4channel_100Hz', 'PA_8channel_100Hz', 'LPDA_2of4_100Hz']
#trigger_names2 = ['PA_4channel_100Hz', 'PA_8channel_100Hz']
trigger_names = ['LPDA_2of4_100Hz']
trigger_names2 = ['PA_8channel_100Hz']

def tmp(filename):

    coincidences = {}
    coincidences['2'] = {}
    coincidences['1'] = {}
    coincidences['weights'] = []

    # Just so I dont have to painfully bring it down to the right tab ...
    if(True): 
        # search for second filename
        filename2 = os.path.join(path2, 
                                 os.path.normpath(filename).split(os.sep)[-3], 
                                 os.path.normpath(filename).split(os.sep)[-2], 
                                 os.path.basename(filename))
    fin = h5py.File(filename, "r")
    fin2 = h5py.File(filename2, "r")

    if not("event_group_ids" in fin.keys()):
        return None
    if not("event_group_ids" in fin2.keys()):
        return None

    ugids1, uindex1 = np.unique(np.array(fin['event_group_ids']), return_index=True)
    ugids2, uindex2 = np.unique(np.array(fin2['event_group_ids']), return_index=True)
    if(len(ugids1) == 0 or len(ugids2) == 0):
        return None

    ugids = np.unique(np.append(ugids1, ugids2))

    ugids_to_index1 = np.zeros(ugids.max() + 1, dtype=np.int)
    ugids_to_index2 = np.zeros(ugids.max() + 1, dtype=np.int)
    ugids_to_index1_single = np.zeros(ugids1.max() + 1, dtype=np.int)
    ugids_to_index2_single = np.zeros(ugids2.max() + 1, dtype=np.int)
    for i, ugid in enumerate(ugids1):
        ugids_to_index1_single[ugid] = i
    for i, ugid in enumerate(ugids2):
        ugids_to_index2_single[ugid] = i
    for i, ugid in enumerate(ugids):
        if(ugid in ugids1):
            ugids_to_index1[ugid] = i
        if(ugid in ugids2):
            ugids_to_index2[ugid] = i

    weights1 = np.array(fin['weights'])[uindex1]  # this gives us the weight per unique group id
    weights2 = np.array(fin2['weights'])[uindex2]  # this gives us the weight per unique group id

    weights = np.zeros(len(ugids))
    for i, ugid in enumerate(ugids):
        if(ugid in ugids1):
            weights[i] = weights1[ugids_to_index1_single[ugid]]
        else:
            weights[i] = weights2[ugids_to_index2_single[ugid]]
    #coincidences['weights'].extend(list(weights))
    coincidences['weights'] = list(weights)

    tnames = fin.attrs['trigger_names']
    tname_to_index = {}
    for i, key in enumerate(tnames):
        tname_to_index[key] = i

    tnames2 = fin2.attrs['trigger_names']
    tname_to_index2 = {}
    for i, key in enumerate(tnames2):
        tname_to_index2[key] = i

    for itname, tname in enumerate(trigger_names):
        #for tname2 in trigger_names2:

        n_stations = np.zeros_like(ugids, dtype=np.int)
        n_stations1 = np.zeros_like(ugids, dtype=np.int)
        n_stations2 = np.zeros_like(ugids, dtype=np.int)

        for key in fin.keys():
            if(key.startswith("station")):
                s = fin[key]
                if("multiple_triggers_per_event" in s):
                    mask = s['multiple_triggers_per_event'][:, tname_to_index[trigger_names[itname]]]
                    s_ugids = np.array(s['event_group_ids'])[mask]
                    n_stations[ugids_to_index1[s_ugids]] += 1
                    n_stations1[ugids_to_index1[s_ugids]] += 1
        for key in fin2.keys():
            if(key.startswith("station")):
                s = fin2[key]
                if("multiple_triggers_per_event" in s):
                    mask = s['multiple_triggers_per_event'][:, tname_to_index2[trigger_names2[itname]]]
                    s_ugids = np.array(s['event_group_ids'])[mask]
                    n_stations[ugids_to_index2[s_ugids]] += 1
                    n_stations2[ugids_to_index2[s_ugids]] += 1
            
        #if tname not in coincidences:
        coincidences[trigger_names[itname]+"_"+trigger_names2[itname]] = list(n_stations)
        coincidences["1"][trigger_names[itname]] = list(n_stations1)
        coincidences["2"][trigger_names2[itname]] = list(n_stations2)
        
        #else:
        #    coincidences[tname].extend(list(n_stations))
        #    coincidences["1"][tname].extend(list(n_stations1))
        #    coincidences["2"][tname].extend(list(n_stations2))

    return coincidences


coincidences = {}
for lgE in np.arange(16.0, 18.1, 0.5):
    coincidences[f"{lgE:.1f}"] = {}
    coincidences[f"{lgE:.1f}"]['2'] = {}
    coincidences[f"{lgE:.1f}"]['1'] = {}
    coincidences[f"{lgE:.1f}"]['weights'] = []

    filenames = glob.glob(os.path.join(path, f"*/*/*_{lgE:.1f}*.hdf5.*"))

    #filenames = filenames[:500]

    with Pool(n_cores) as p:
        pool_result = p.map(tmp, filenames)

    for result in pool_result:
        if(result is None):
            continue

        coincidences[f"{lgE:.1f}"]['weights'].extend(result['weights'])

        for itname, tname in enumerate(trigger_names):
            #for tname2 in trigger_names2:

            combo = trigger_names[itname]+"_"+trigger_names2[itname]

            if combo not in coincidences[f"{lgE:.1f}"]:
                coincidences[f"{lgE:.1f}"][combo] = result[combo]
                coincidences[f"{lgE:.1f}"]["1"][trigger_names[itname]] = result["1"][trigger_names[itname]]
                coincidences[f"{lgE:.1f}"]["2"][trigger_names2[itname]] = result["2"][trigger_names2[itname]]
            else:
                coincidences[f"{lgE:.1f}"][combo].extend(result[combo])
                coincidences[f"{lgE:.1f}"]["1"][trigger_names[itname]].extend(result["1"][trigger_names[itname]])
                coincidences[f"{lgE:.1f}"]["2"][trigger_names2[itname]].extend(result["2"][trigger_names2[itname]])
        
    #if(len(coincidences[f"{lgE:.1f}"][tname]) != len(coincidences[f"{lgE:.1f}"]['weights'])):
    #    a = 1 / 0

with open(os.path.join(path.split("/")[-5] + path2.split("/")[-5] + ".pkl"), "wb") as fout:
    print(os.path.join(path.split("/")[-5] + path2.split("/")[-5] + ".pkl"))
    pickle.dump(coincidences, fout, protocol=4)

print(f"trigger names {trigger_names}")
for lgE, value in coincidences.items():
    print(f"E = 10^{lgE}eV")

    if(tname not in value):
        continue

    for i in range(2, 5):
        output = f"\t>= {i} station coincidences: "
        for tname in trigger_names:
            n_stations = np.array(value[tname])
            n_stations1 = np.array(coincidences[lgE]["1"][tname])
            n_stations2 = np.array(coincidences[lgE]["2"][tname])
            n_stations_dual = n_stations1 * n_stations2
            n_tot = np.sum(n_stations > 0)
            weights = np.array(coincidences[lgE]['weights'])
            fraction = np.sum(n_stations >= i) / n_tot
            fraction_w = np.sum(weights[n_stations >= i]) / np.sum(weights[n_stations > 0])
            fraction_w_1 = np.sum(weights[n_stations1 >= i]) / np.sum(weights[n_stations1 > 0])
            fraction_w_2 = np.sum(weights[n_stations2 >= i]) / np.sum(weights[n_stations2 > 0])
            fraction_w_dual = np.sum(weights[n_stations_dual >= i]) / np.sum(weights[n_stations > 0])
            output += f"\t{fraction*100:.1f}% ({fraction_w*100:.1f}%), dual = {fraction_w_dual* 100:.1f}%, , 1 = {fraction_w_1* 100:.1f}%, , 2 = {fraction_w_2* 100:.1f}%"
        print(output)

