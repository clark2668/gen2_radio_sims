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

from NuRadioReco.utilities import units
# plt.switch_backend('agg')

path = sys.argv[1]
path2 = sys.argv[2]
trigger_names = sys.argv[3:]
# trigger_names = ["LPDA_2of4_100Hz", "dipole_2.5sigma", "dipole_1.5sigma"]

coincidences = {}
weights_dict = {}
for lgE in np.arange(18.5, 19.1, 0.5):
    coincidences[f"{lgE:.1f}"] = {}
    coincidences[f"{lgE:.1f}"]['2'] = {}
    coincidences[f"{lgE:.1f}"]['1'] = {}
    coincidences[f"{lgE:.1f}"]['weights'] = []
    filenames = glob.glob(os.path.join(path, f"e/*{lgE:.2f}eV_*.hdf5"))
    for filename in filenames:
        print('working on file {}'.format(filename))
        # search for second filename
        filename2 = os.path.join(path2, os.path.normpath(filename).split(os.sep)[-2], os.path.basename(filename))
        fin = h5py.File(filename, "r")
        fin2 = h5py.File(filename2, "r")
        if not("event_group_ids" in fin.keys()):
            continue
        if not("event_group_ids" in fin2.keys()):
            continue

        ugids1, uindex1 = np.unique(np.array(fin['event_group_ids']), return_index=True)
        ugids2, uindex2 = np.unique(np.array(fin2['event_group_ids']), return_index=True)
        if(len(ugids1) == 0 or len(ugids2) == 0):
            continue

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
        coincidences[f"{lgE:.1f}"]['weights'].extend(list(weights))

        tnames = fin.attrs['trigger_names']
        tname_to_index = {}
        for i, key in enumerate(tnames):
            tname_to_index[key] = i

        tnames2 = fin2.attrs['trigger_names']
        tname_to_index2 = {}
        for i, key in enumerate(tnames2):
            tname_to_index2[key] = i

        for tname in trigger_names:
            n_stations = np.zeros_like(ugids, dtype=np.int)
            n_stations1 = np.zeros_like(ugids, dtype=np.int)
            n_stations2 = np.zeros_like(ugids, dtype=np.int)
            for key in fin.keys():
                if(key.startswith("station")):
                    s = fin[key]
                    if("multiple_triggers_per_event" in s):
                        mask = s['multiple_triggers_per_event'][:, tname_to_index[tname]]
                        s_ugids = np.array(s['event_group_ids'])[mask]
                        n_stations[ugids_to_index1[s_ugids]] += 1
                        n_stations1[ugids_to_index1[s_ugids]] += 1
            for key in fin2.keys():
                if(key.startswith("station")):
                    s = fin2[key]
                    if("multiple_triggers_per_event" in s):
                        mask = s['multiple_triggers_per_event'][:, tname_to_index2[tname]]
                        s_ugids = np.array(s['event_group_ids'])[mask]
                        n_stations[ugids_to_index2[s_ugids]] += 1
                        n_stations2[ugids_to_index2[s_ugids]] += 1
            if tname not in coincidences[f"{lgE:.1f}"]:
                coincidences[f"{lgE:.1f}"][tname] = list(n_stations)
                coincidences[f"{lgE:.1f}"]["1"][tname] = list(n_stations1)
                coincidences[f"{lgE:.1f}"]["2"][tname] = list(n_stations2)
            else:
                coincidences[f"{lgE:.1f}"][tname].extend(list(n_stations))
                coincidences[f"{lgE:.1f}"]["1"][tname].extend(list(n_stations1))
                coincidences[f"{lgE:.1f}"]["2"][tname].extend(list(n_stations2))
    # if(len(coincidences[f"{lgE:.1f}"][tname]) != len(coincidences[f"{lgE:.1f}"]['weights'])):
    #     a = 1 / 0

with open(os.path.join("christian.pkl"), "wb") as fout:
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

