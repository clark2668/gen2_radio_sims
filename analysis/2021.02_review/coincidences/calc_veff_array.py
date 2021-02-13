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

# a version of the coincidence finding code that tries to sync up which stations are on top of which

n_cores = 10

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
s_d_match = {}
for i in range(len(matching_data)):
	s_d_match[int(matching_data['shallowID'][i])] = int(matching_data['deepID'][i])

good_deep = np.genfromtxt('good_deep.csv', delimiter=',', skip_header=0, names=['ID'])
good_deep = good_deep['ID']
good_shallow = np.genfromtxt('good_shallow.csv', delimiter=',', skip_header=0, names=['ID'])
good_shallow = good_shallow['ID']

# print('num deep {}'.format(len(good_deep)))
# print('num shallow {}'.format(len(good_shallow)))

def tmp(filename):

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

	# our goal is to figure out
	# first, how many events triggered in either the deep or the surface array
	# second, how many events triggered in just the deep array, just the surface array, or both
	# so, we will make a dictionary  of information
	# for every event (key), we will store an array (values)
	# the array will contain a weight
	# if it triggers at all
	# if it triggers deep, triggers shallow, or triggers both
	event_information = {}

	# first, get the group ids of the events that triggered either in deep or in shallow

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

	# first, the deep station
	for key in fin.keys():
		if(key.startswith("station")):
			deep_id = int(key.split("_")[1]) # get the deep id
			if deep_id not in good_deep: # skip detectors not in the review array
				continue
			s_deep = fin[f'station_{deep_id}']
			if 'multiple_triggers_per_event' in s_deep:
				triggers_deep = s_deep['multiple_triggers_per_event'][:, tname_to_index[trigger_names[0]]]
				evs_triggers_deep = np.unique(np.array(s_deep['event_group_ids'])[triggers_deep])

				for ev in evs_triggers_deep:
					if ev not in event_information:
						event_information[ev] = [weights_dict_deep[ev], 0, 0]
						event_information[ev][1] = 1 # mark that it is seen in SOME deep station
						# (0) store the weight, (1) seen in ANY deep, (2) seen in ANY shallow

	for key in fin2.keys():
		if(key.startswith("station")):
			shallow_id = int(key.split("_")[1]) # get the shallow id
			if shallow_id not in good_shallow: # skip the detectors not in the review array
				continue
			s_shallow = fin2[f'station_{shallow_id}']
			if 'multiple_triggers_per_event' in s_shallow:
				triggers_shallow = s_shallow['multiple_triggers_per_event'][:, tname_to_index2[trigger_names[0]]]
				evs_triggers_shallow = np.unique(np.array(s_shallow['event_group_ids'])[triggers_shallow])

				for ev in evs_triggers_shallow:
					if ev not in event_information:
						event_information[ev] = [weights_dict_shallow[ev], 0, 0]
						event_information[ev][2] = 1 # mark that it is seen in SOME shallow station
					elif ev in event_information:
						event_information[ev][2]=1

	tot_weight = 0
	deep_only_weight = 0
	shallow_only_weight = 0
	dual_weight = 0

	for ev in event_information:
		weight = event_information[ev][0]
		trig_deep = event_information[ev][1]
		trig_shal = event_information[ev][2]

		tot_weight+=weight
		if trig_deep and trig_shal:
			# print('Mutual: {}, {}'.format(trig_deep, trig_shal))
			dual_weight+=weight
		elif trig_deep and not trig_shal:
			# print('Deep: {}, {}'.format(trig_deep, trig_shal))
			deep_only_weight+=weight
		elif trig_shal and not trig_deep:
			# print('Shallow: {}, {}'.format(trig_deep, trig_shal))
			shallow_only_weight+=weight

	# print("Total weight {}".format(tot_weight))
	# print("Deep only weight {}".format(deep_only_weight))
	# print("Shallow only weight {}".format(shallow_only_weight))
	# print("Dual weight {}".format(dual_weight))
	# print("Sum: {}".format(deep_only_weight + shallow_only_weight + dual_weight))

	summary = {}
	summary['n_events'] = fin.attrs['n_events']
	summary['volume'] = fin.attrs['volume']
	summary['czmin'] = np.cos(fin.attrs['thetamin'])
	summary['czmax'] = np.cos(fin.attrs['thetamax'])
	summary['tot_weight'] = tot_weight
	summary['deep_only_weight'] = deep_only_weight
	summary['shallow_only_weight'] = shallow_only_weight
	summary['dual_weight'] = dual_weight

	return summary

flavors = ['e', 'mu', 'tau']
for flavor in flavors:
	total_veff = {}
	for lgE in np.arange(16.0, 20.1, 0.5):
	# for lgE in np.arange(18.0, 18.4, 0.5):
		total_veff[f"{lgE:.1f}"] = {}
		
		combined_total_veff = 0
		combined_deep_only_veff = 0
		combined_shallow_only_veff = 0
		combined_dual_veff = 0
		num_zen_bins = 0

		# local_path = os.path.join(path, f"{flavor}/{flavor}_{lgE:.2f}*_0.3_*.hdf5")
		local_path = os.path.join(path, f"{flavor}/{flavor}_{lgE:.2f}*.hdf5")
		filenames = glob.glob(local_path)

		with Pool(n_cores) as p:
			pool_result = p.map(tmp, filenames)

		for result in pool_result:
			if(result is None):
				continue

			combined_total_veff += result['tot_weight']/result['n_events'] * result['volume']
			combined_deep_only_veff += result['deep_only_weight']/result['n_events'] * result['volume']
			combined_shallow_only_veff += result['shallow_only_weight']/result['n_events'] * result['volume']
			combined_dual_veff += result['dual_weight']/result['n_events'] * result['volume']
			num_zen_bins+=1

		num_zen_bins=20 # override

		print("num zen bins {}".format(num_zen_bins))
		total_veff[f"{lgE:.1f}"]['total_veff'] = gwe(combined_total_veff/num_zen_bins)
		total_veff[f"{lgE:.1f}"]['deep_only_veff'] = gwe(combined_deep_only_veff/num_zen_bins)
		total_veff[f"{lgE:.1f}"]['shallow_only_veff'] = gwe(combined_shallow_only_veff/num_zen_bins)
		total_veff[f"{lgE:.1f}"]['dual_veff'] = gwe(combined_dual_veff/num_zen_bins)

		print("dual veff at 1 EeV for {} is {}".format(total_veff[f"{lgE:.1f}"]['total_veff']/units.km**3 * 4 * np.pi, flavor))

	# dump this to hdf5 file
	pkl_file_name = os.path.join('overlap_' + path.split("/")[-4] + "_" + trigger_names[0] + "_" + path2.split("/")[-4] + "_" + trigger_names2[0] + "_" + flavor + ".pkl")
	with open(pkl_file_name, "wb") as fout:
		pickle.dump(total_veff, fout, protocol=4)
