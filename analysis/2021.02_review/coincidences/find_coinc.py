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

n_cores = 8

top="/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step4/"

path = top+"/pa_200m_2.00km/config_Alv2009_noise_100ns/D05phased_array_deep/"
path2 = top+"/surface_4LPDA_PA_15m_RNOG_300K_1.00km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/"

#trigger_names = ['PA_4channel_100Hz', 'PA_8channel_100Hz', 'LPDA_2of4_100Hz']
#trigger_names2 = ['PA_4channel_100Hz', 'PA_8channel_100Hz']
trigger_names2 = ['LPDA_2of4_100Hz']
trigger_names = ['PA_4channel_100Hz']

def tmp(filename):

	coincidences = {}
	coincidences['2'] = {}
	coincidences['1'] = {}
	coincidences['weights'] = []

	# Just so I dont have to painfully bring it down to the right tab ...
	if(True): 
		# search for second filename
		filename2 = os.path.join(path2, 
								 os.path.normpath(filename).split(os.sep)[-2], 
								 os.path.normpath(filename).split(os.sep)[-1])
	
	print("Working on file {}".format(filename))

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

	ugids = np.unique(np.append(ugids1, ugids2)) # make a unique list

	ugids_to_index1 = np.zeros(ugids.max() + 1, dtype=np.int) # make a bunch of zeros--as many of them as the highest triggered shower in the unique group set
	ugids_to_index2 = np.zeros(ugids.max() + 1, dtype=np.int) # make a bunch of zeros--as many of them as the highest triggered shower in the unique group set
	ugids_to_index1_single = np.zeros(ugids1.max() + 1, dtype=np.int) # make a bunch of zeros--as many of them as the highest triggered shower in file 1
	ugids_to_index2_single = np.zeros(ugids2.max() + 1, dtype=np.int) # make a bunch of zeros--as many of them as the highest triggered shower in file 2

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

		n_stations = np.zeros_like(ugids, dtype=np.int)
		n_stations1 = np.zeros_like(ugids, dtype=np.int)
		n_stations2 = np.zeros_like(ugids, dtype=np.int)

		# for the first file, figure out how many stations registered a trigger for each neutrino
		for key in fin.keys():
			if(key.startswith("station")):
				s = fin[key] # get the group (in an hdf5 sense) of information for this station
				if("multiple_triggers_per_event" in s):

					# pull the mask for this station--e.g. which events had this trigger?
					mask = s['multiple_triggers_per_event'][:, tname_to_index[trigger_names[itname]]]
					
					# apply that mask so we only keep the unique group ids for this station that caused a trigger
					s_ugids = np.array(s['event_group_ids'])[mask]
					n_stations[ugids_to_index1[s_ugids]] += 1
					n_stations1[ugids_to_index1[s_ugids]] += 1

		# do the same for the second file--how many stations registered a trigger for each neutrino
		for key in fin2.keys():
			if(key.startswith("station")):
				s = fin2[key]
				if("multiple_triggers_per_event" in s):
					mask = s['multiple_triggers_per_event'][:, tname_to_index2[trigger_names2[itname]]]
					s_ugids = np.array(s['event_group_ids'])[mask]
					n_stations[ugids_to_index2[s_ugids]] += 1
					n_stations2[ugids_to_index2[s_ugids]] += 1
			
		coincidences[trigger_names[itname]+"_"+trigger_names2[itname]] = list(n_stations)
		coincidences["1"][trigger_names[itname]] = list(n_stations1)
		coincidences["2"][trigger_names2[itname]] = list(n_stations2)
		
	return coincidences



flavors = ['mu']
for flavor in flavors:
	coincidences = {}
	for lgE in np.arange(18.5, 20.1, 0.5):
		coincidences[f"{lgE:.1f}"] = {}
		coincidences[f"{lgE:.1f}"]['2'] = {}
		coincidences[f"{lgE:.1f}"]['1'] = {}
		coincidences[f"{lgE:.1f}"]['weights'] = []

		local_path = os.path.join(path, f"{flavor}/{flavor}_{lgE:.2f}*.hdf5")
		filenames = glob.glob(local_path)

		with Pool(n_cores) as p:
			pool_result = p.map(tmp, filenames)

		for result in pool_result:
			if(result is None):
				continue

			coincidences[f"{lgE:.1f}"]['weights'].extend(result['weights'])

			for itname, tname in enumerate(trigger_names):

				combo = trigger_names[itname]+"_"+trigger_names2[itname]

				# if we haven't already stored this combo (which is unlikely in the way this script is written)
				# then write it down
				if combo not in coincidences[f"{lgE:.1f}"]:
					coincidences[f"{lgE:.1f}"][combo] = result[combo]
					coincidences[f"{lgE:.1f}"]["1"][trigger_names[itname]] = result["1"][trigger_names[itname]]
					coincidences[f"{lgE:.1f}"]["2"][trigger_names2[itname]] = result["2"][trigger_names2[itname]]
				else:
					coincidences[f"{lgE:.1f}"][combo].extend(result[combo])
					coincidences[f"{lgE:.1f}"]["1"][trigger_names[itname]].extend(result["1"][trigger_names[itname]])
					coincidences[f"{lgE:.1f}"]["2"][trigger_names2[itname]].extend(result["2"][trigger_names2[itname]])
			
	# dump this to hdf5 file
	pkl_file_name = os.path.join(path.split("/")[-4] + "_" + trigger_names[0] + "_" + path2.split("/")[-4] + "_" + trigger_names2[0] + "_" + flavor + ".pkl")
	with open(pkl_file_name, "wb") as fout:
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
