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

# a version of the coincidence finding code that tries to sync up which stations are on top of which

n_cores = 4

top="/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step4/"

path = top+"/pa_200m_2.00km/config_Alv2009_noise_100ns/D05phased_array_deep/"
# path = top+"/surface_4LPDA_PA_15m_RNOG_300K_1.00km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/" ## TEST--delete me!

path2 = top+"/surface_4LPDA_PA_15m_RNOG_300K_1.00km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/"
# path2 = top+"/pa_200m_2.00km/config_Alv2009_noise_100ns/D05phased_array_deep/" ## TEST -- delete me

trigger_names = ['PA_4channel_100Hz']
# trigger_names = ['LPDA_2of4_100Hz'] ## TEST--delete me!
trigger_names2 = ['LPDA_2of4_100Hz'] 
# trigger_names2 = ['PA_4channel_100Hz'] ## TEST--delete me!

# get the deep/surface mapping, as a dict to make loop easier
matching_data = np.genfromtxt('deep_shallow_match.csv', delimiter=',', skip_header=0, names=['deepID', 'shallowID'])
d_s_match = {}
for i in range(len(matching_data)):
	d_s_match[int(matching_data['deepID'][i])] = int(matching_data['shallowID'][i])

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

	# so, what we need to do is:
	# 1. Go through every deep station
	# 2. Go through every trigger in the deep station
	# 3. Figure out if the corresponding shallow station also saw something for that event
	# 4. If so, record the weight of that event as a "dual trigger"

	tot_weight_deep = 0 # total weight of events observed in the deep detector
	tot_weight_shallow = 0 # total weight of events observed in the shallow detector
	overlap_weight = 0 # total weight of the events observed in both the deep and shallow detector

	ugids1, uindex1 = np.unique(np.array(fin['event_group_ids']), return_index=True)
	ugids2, uindex2 = np.unique(np.array(fin2['event_group_ids']), return_index=True)
	if(len(ugids1) == 0 or len(ugids2) == 0):
		return None

	weights1 = np.array(fin['weights'])[uindex1]  # this gives us the weight per unique group id
	weights2 = np.array(fin2['weights'])[uindex2]  # this gives us the weight per unique group id

	weights_dict_deep = {A:B for A, B in zip(ugids1, weights1)}
	weights_dict_shallow = {A:B for A, B in zip(ugids2, weights2)}

	tnames = fin.attrs['trigger_names']
	tname_to_index = {}
	for i, key in enumerate(tnames):
		tname_to_index[key] = i

	tnames2 = fin2.attrs['trigger_names']
	tname_to_index2 = {}
	for i, key in enumerate(tnames2):
		tname_to_index2[key] = i

	for itname, tname in enumerate(trigger_names):

		# for the first file, figure out how many stations registered a trigger for each neutrino
		for key in fin.keys():
			if(key.startswith("station")):

				# figure out the deep/shallow pairing (based on deep station)
				deep_id = int(key.split("_")[1])
				shallow_id = d_s_match[deep_id]
				# shallow_id = deep_id ## TEST -- delete me!

				# get the information for both stations
				s_deep = fin[f'station_{deep_id}']
				s_shallow = fin2[f'station_{shallow_id}']

				if('multiple_triggers_per_event' in s_deep) and ('multiple_triggers_per_event' in s_shallow):

					triggers_deep = s_deep['multiple_triggers_per_event'][:, tname_to_index[trigger_names[0]]]
					triggers_shallow = s_shallow['multiple_triggers_per_event'][:, tname_to_index2[trigger_names2[0]]]

					# make sure to force them to be unique
					evs_triggers_deep = np.unique(np.array(s_deep['event_group_ids'])[triggers_deep])
					evs_triggers_shallow = np.unique(np.array(s_shallow['event_group_ids'])[triggers_shallow])
					# print('Deep {}'.format(evs_triggers_deep))
					# print('Shallow {}'.format(evs_triggers_shallow))

					for ev in evs_triggers_deep:
						tot_weight_deep+=weights_dict_deep[ev]

					for ev in evs_triggers_shallow:
						tot_weight_shallow+=weights_dict_shallow[ev]

					overlap_evs = np.intersect1d(evs_triggers_deep, evs_triggers_shallow)
					for ev in overlap_evs:
						overlap_weight+=weights_dict_deep[ev]
					
		# print("Overlap fraction deep: {:e}/{:e} = {:.2f}".format(overlap_weight, tot_weight_deep, overlap_weight/tot_weight_deep))
		# print("Overlap fraction shallow: {:e}/{:e} = {:.2f}".format(overlap_weight, tot_weight_shallow, overlap_weight/tot_weight_shallow))
		return [overlap_weight, tot_weight_deep, tot_weight_shallow]

flavors = ['tau']
for flavor in flavors:
	coincidences = {}
	for lgE in np.arange(16.0, 20.1, 0.5):
	# for lgE in np.arange(18.0, 18.4, 0.5):
		coincidences[f"{lgE:.1f}"] = {}

		# local_path = os.path.join(path, f"{flavor}/{flavor}_{lgE:.2f}*_0.*_*.hdf5")
		local_path = os.path.join(path, f"{flavor}/{flavor}_{lgE:.2f}*.hdf5")
		filenames = glob.glob(local_path)

		with Pool(n_cores) as p:
			pool_result = p.map(tmp, filenames)

		combined_overlap_weight = 0
		combined_tot_weight_deep = 0 
		combined_tot_weight_shallow = 0

		for result in pool_result:
			if(result is None):
				continue

			combined_overlap_weight+=result[0]
			combined_tot_weight_deep+=result[1]
			combined_tot_weight_shallow+=result[2]

		coincidences[f"{lgE:.1f}"]['overlap_weight'] = combined_overlap_weight
		coincidences[f"{lgE:.1f}"]['deep_weight'] = combined_tot_weight_deep
		coincidences[f"{lgE:.1f}"]['shallow_weight'] = combined_tot_weight_shallow

	print("Overlap {}, Deep {}, Shallow {}, Deep Overlap {}".format(combined_overlap_weight, combined_tot_weight_deep, combined_tot_weight_shallow, combined_overlap_weight/combined_tot_weight_deep))

	# dump this to hdf5 file
	pkl_file_name = os.path.join('coinc_' + path.split("/")[-4] + "_" + trigger_names[0] + "_" + path2.split("/")[-4] + "_" + trigger_names2[0] + "_" + flavor + ".pkl")
	with open(pkl_file_name, "wb") as fout:
		pickle.dump(coincidences, fout, protocol=4)
