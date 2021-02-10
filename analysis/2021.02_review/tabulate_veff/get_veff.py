import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
import sys

from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
# from NuRadioReco.detector import detector
# from NuRadioMC.utilities import fluxes
from NuRadioMC.utilities.Veff import  get_Veff_Aeff_array, get_index, get_Veff_water_equivalent
# from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
# from astropy import coordinates as coord
# from NuRadioMC.utilities import cross_sections
import pickle
import copy

flavors = ['e', 'mu', 'tau']

def get_flavor_zenith_averages(det, det_dict): # det ('deep') and the associated dictionary
	
	if 'trigger' not in det_dict.keys():
		print("A trigger is not specified")
	trigger = det_dict['trigger']
	
	tmp = {} # a holder
	tmp[trigger] = {}

	for iF, flavor in enumerate(flavors):

		# first, the low energies
		filename = f'data/{det}_{flavor}_lo.pkl'
		data = pickle.load(open(filename, 'br'))
		output, energies, energies_low, energies_up, zenith_bins, trigger_names = get_Veff_Aeff_array(data)

		if trigger not in trigger_names:
			print("The requested trigger is not available. Options are {}".format(trigger_names))

		tmp['E'] = energies
		tmp[trigger][flavor] = {}
		tmp[trigger][flavor]['Veff_zen'] = output[:, :, get_index(trigger, trigger_names), 0]
		tmp[trigger][flavor]['Veff'] = np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)
		tmp[trigger][flavor]['Vefferror'] = tmp[trigger][flavor]['Veff'] / np.sum(output[:, :, get_index(trigger, trigger_names), 2], axis=1) ** 0.5
		tmp[trigger][flavor]['Vefferror_up'] = np.sum((output[:, :, get_index(trigger, trigger_names), 4] - output[:, :, get_index(trigger, trigger_names), 0]) ** 2, axis=1) ** 0.5 / output.shape[1]
		tmp[trigger][flavor]['Vefferror_down'] = np.sum((output[:, :, get_index(trigger, trigger_names), 0] - output[:, :, get_index(trigger, trigger_names), 3]) ** 2, axis=1) ** 0.5 / output.shape[1]

		# now, the high energies
		filename = f'data/{det}_{flavor}_hi.pkl'
		data = pickle.load(open(filename, 'br'))
		output, energies, energies_low, energies_up, zenith_bins, trigger_names = get_Veff_Aeff_array(data)

		if trigger not in trigger_names:
			print("The requested trigger is not available. Options are {}".format(trigger_names))

		tmp['E'] = np.append(tmp['E'], energies)  # we assume we have the same energies simulated for each flavor
		tmp[trigger][flavor]['Veff_zen'] = np.append(tmp[trigger][flavor]['Veff_zen'], output[:, :, get_index(trigger, trigger_names), 0])
		tmp[trigger][flavor]['Veff'] = np.append(tmp[trigger][flavor]['Veff'], np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1))
		tmp[trigger][flavor]['Vefferror'] = np.append(tmp[trigger][flavor]['Vefferror'], np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1) / np.sum(output[:, :, get_index(trigger, trigger_names), 2], axis=1) ** 0.5)
		tmp[trigger][flavor]['Vefferror_up'] = np.append(tmp[trigger][flavor]['Vefferror_up'], np.sum((output[:, :, get_index(trigger, trigger_names), 4] - output[:, :, get_index(trigger, trigger_names), 0]) ** 2, axis=1) ** 0.5 / output.shape[1])
		tmp[trigger][flavor]['Vefferror_down'] = np.append(tmp[trigger][flavor]['Vefferror_down'], np.sum((output[:, :, get_index(trigger, trigger_names), 0] - output[:, :, get_index(trigger, trigger_names), 3]) ** 2, axis=1) ** 0.5 / output.shape[1])

	# do the flavor average
	tmp[trigger]['Veff'] = 0
	tmp[trigger]['Vefferror'] = 0
	tmp[trigger]['Vefferror_down'] = 0
	tmp[trigger]['Vefferror_up'] = 0
	tmp[trigger]['Veff_zen'] = 0
	for flavor in flavors:
	    tmp[trigger]['Veff'] += tmp[trigger][flavor]['Veff']
	    tmp[trigger]['Vefferror'] += tmp[trigger][flavor]['Vefferror']
	    tmp[trigger]['Veff_zen'] += tmp[trigger][flavor]['Veff_zen']
	    tmp[trigger]['Vefferror_up'] += tmp[trigger][flavor]['Vefferror_up'] ** 2
	    tmp[trigger]['Vefferror_down'] += tmp[trigger][flavor]['Vefferror_down'] ** 2
	tmp[trigger]['Vefferror'] /= 3
	tmp[trigger]['Veff_zen'] /= 3
	tmp[trigger]['Veff'] /= 3
	tmp[trigger]['Vefferror_up'] = tmp[trigger]['Vefferror_up'] ** 0.5 / 3
	tmp[trigger]['Vefferror_down'] = tmp[trigger]['Vefferror_down'] ** 0.5 / 3

	return tmp

if __name__ == "__main__":

	r = {'shallow': {}, 'deep': {}} # dictionary of dictionaries for shallow and deep stations
	r['shallow']['n_stations'] = 546 # 546 surface stations
	r['shallow']['trigger'] = 'LPDA_2of4_100Hz' # the shallow trigger
	r['deep']['n_stations'] = 143 # 143 deep stations
	r['deep']['trigger'] = 'PA_4channel_100Hz' # the deep trigger


	keys = list(r.keys()) # get the keys, which should at this point just return 's' and 'd'
	for d in keys:
		r[d]['Veff'] = get_flavor_zenith_averages(d, r[d]) # get the veff


	energies = r['shallow']['Veff']['E']
	deep_veff = []
	deep_aeff = []
	shallow_veff = []
	shallow_aeff = []

	# first the deep station
	det = 'deep'
	trigger = r[det]['trigger']
	for veff, energy in zip(r[det]['Veff'][trigger]['Veff'], energies):
		this_veff = get_Veff_water_equivalent(veff / r[det]['n_stations'] * 4 * np.pi)
		this_aeff = this_veff / cross_sections.get_interaction_length(energy)
		deep_veff.append(this_veff/units.km**3)
		deep_aeff.append(this_aeff/units.km**2)

	det = 'shallow'
	trigger = r[det]['trigger']
	for veff, energy in zip(r[det]['Veff'][trigger]['Veff'], energies):
		this_veff = get_Veff_water_equivalent(veff / r[det]['n_stations'] * 4 * np.pi)
		this_aeff = this_veff / cross_sections.get_interaction_length(energy)
		shallow_veff.append(this_veff/units.km**3)
		shallow_aeff.append(this_aeff/units.km**2)


	output_csv = 'log10(energy) [eV], deep veff*sr [km^3sr], deep aeff*sr [km^2sr], shallow veff*sr [km^3sr], shallow aeff*str [km^2sr]'
	output_csv += "\n"

	for iE, energy in enumerate(energies):
		output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e} \n'.format(np.log10(energy), deep_veff[iE], deep_aeff[iE], shallow_veff[iE], shallow_aeff[iE])

	with open(f'tabulated_veff_aeff.csv', 'w') as fout:
		fout.write(output_csv)









