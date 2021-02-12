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

deep_det = 'pa_200m_2.00km'
shallow_det = 'surface_1.00km'
flavors = ['e', 'mu', 'tau']

if shallow_det=='surface_1.50km':
	print("WARNING! Something is known to be funky with the 1.50km files... Advise avoiding for now....")

def get_flavor_zenith_averages(det, det_dict): # det ('deep') and the associated dictionary
	
	if 'trigger' not in det_dict.keys():
		print("A trigger is not specified")
	trigger = det_dict['trigger']
	
	tmp = {} # a holder
	tmp[trigger] = {}

	for iF, flavor in enumerate(flavors):

		# first, the low energies
		filename = f'data__{deep_det}__{shallow_det}/{det}_{flavor}_lo.pkl'
		data = pickle.load(open(filename, 'br'))
		output, energies, energies_low, energies_up, zenith_bins, trigger_names = get_Veff_Aeff_array(data)

		if trigger not in trigger_names:
			print("The requested trigger is not available. Options are {}".format(trigger_names))
		tmp['E'] = energies
		tmp['zen_bins']=zenith_bins
		tmp[trigger][flavor] = {}
		tmp[trigger][flavor]['Veff_zen'] = output[:, :, get_index(trigger, trigger_names), 0]
		tmp[trigger][flavor]['Veff'] = np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)
		tmp[trigger][flavor]['Vefferror'] = tmp[trigger][flavor]['Veff'] / np.sum(output[:, :, get_index(trigger, trigger_names), 2], axis=1) ** 0.5
		tmp[trigger][flavor]['Vefferror_up'] = np.sum((output[:, :, get_index(trigger, trigger_names), 4] - output[:, :, get_index(trigger, trigger_names), 0]) ** 2, axis=1) ** 0.5 / output.shape[1]
		tmp[trigger][flavor]['Vefferror_down'] = np.sum((output[:, :, get_index(trigger, trigger_names), 0] - output[:, :, get_index(trigger, trigger_names), 3]) ** 2, axis=1) ** 0.5 / output.shape[1]

		# print("low energy energies {}".format(energies))
		# print("low energy veffs {}".format(np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)))
		# print("low energy veffs vs zen {}".format(output[:, :, get_index(trigger, trigger_names), 0]))

		# now, the high energies
		filename = f'data__{deep_det}__{shallow_det}/{det}_{flavor}_hi.pkl'
		data = pickle.load(open(filename, 'br'))
		output, energies, energies_low, energies_up, zenith_bins, trigger_names = get_Veff_Aeff_array(data)

		if trigger not in trigger_names:
			print("The requested trigger is not available. Options are {}".format(trigger_names))

		# Brian did something silly, and for the 1.5km station, his files accidentally contain an incorrect calculation for the low energies
		# so we need to splice those away, which are index 0 (1E16), 1 (1E16.5), 2 (1E17), 3 (1E17.5), 4 (1E18)
		start_splice_index=0
		if flavor=='mu' and det=='shallow' and shallow_det=='surface_1.50km':
			start_splice_index=5

		tmp['E'] = np.append(tmp['E'], energies[start_splice_index:])  # we assume we have the same energies simulated for each flavor
		tmp[trigger][flavor]['Veff_zen'] = np.append(tmp[trigger][flavor]['Veff_zen'], output[:, :, get_index(trigger, trigger_names), 0][start_splice_index:])
		tmp[trigger][flavor]['Veff'] = np.append(tmp[trigger][flavor]['Veff'], np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)[start_splice_index:])
		tmp[trigger][flavor]['Vefferror'] = np.append(tmp[trigger][flavor]['Vefferror'], np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)[start_splice_index:] / np.sum(output[:, :, get_index(trigger, trigger_names), 2], axis=1)[start_splice_index:] ** 0.5)
		tmp[trigger][flavor]['Vefferror_up'] = np.append(tmp[trigger][flavor]['Vefferror_up'], np.sum((output[:, :, get_index(trigger, trigger_names), 4] - output[:, :, get_index(trigger, trigger_names), 0])[start_splice_index:] ** 2, axis=1) ** 0.5 / output.shape[1])
		tmp[trigger][flavor]['Vefferror_down'] = np.append(tmp[trigger][flavor]['Vefferror_down'], np.sum((output[:, :, get_index(trigger, trigger_names), 0] - output[:, :, get_index(trigger, trigger_names), 3])[start_splice_index:] ** 2, axis=1) ** 0.5 / output.shape[1])

		# print("high energy energies {}".format(energies[start_splice_index:]))
		# print("high energy veffs {}".format(np.average(output[:, :, get_index(trigger, trigger_names), 0], axis=1)[start_splice_index:]))
		# print("\n")

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
	zen_bins = r['shallow']['Veff']['zen_bins']
	deep_veff = []
	deep_aeff = []
	shallow_veff = []
	shallow_aeff = []

	if len(energies)!=11:
		print("I expected 11 energy bins...You may not get the zenith bins you expected...")
	which_e_bin = 6 # should be 1 EeV, counting from 0 = 1E15
	start_bin = which_e_bin*20
	stop_bin = start_bin+20

	# first the deep station
	det = 'deep'
	trigger = r[det]['trigger']
	for veff, energy in zip(r[det]['Veff'][trigger]['Veff'], energies):
		this_veff = get_Veff_water_equivalent(veff / r[det]['n_stations'] * 4 * np.pi)
		this_aeff = this_veff / cross_sections.get_interaction_length(energy)
		deep_veff.append(this_veff/units.km**3)
		deep_aeff.append(this_aeff/units.km**2)
	
	# and now for aeff for a selection of the zenith bins
	deep_veff_vs_zen = get_Veff_water_equivalent(r[det]['Veff'][trigger]['Veff_zen'][start_bin:stop_bin]/r[det]['n_stations'])
	deep_aeff_vs_zen = deep_veff_vs_zen / cross_sections.get_interaction_length(energies[which_e_bin])/ units.km**2
	# print("deep veff vs zen {}".format(deep_veff_vs_zen))

	det = 'shallow'
	trigger = r[det]['trigger']
	for veff, energy in zip(r[det]['Veff'][trigger]['Veff'], energies):
		this_veff = get_Veff_water_equivalent(veff / r[det]['n_stations'] * 4 * np.pi)
		this_aeff = this_veff / cross_sections.get_interaction_length(energy)
		shallow_veff.append(this_veff/units.km**3)
		shallow_aeff.append(this_aeff/units.km**2)

	# and now for aeff for a selection of the zenith bins
	shallow_veff_vs_zen = get_Veff_water_equivalent(r[det]['Veff'][trigger]['Veff_zen'][start_bin:stop_bin]/r[det]['n_stations'])
	shallow_aeff_vs_zen = shallow_veff_vs_zen / cross_sections.get_interaction_length(energies[which_e_bin]) / units.km**2
	# print("shallow veff vs zen {}".format(shallow_veff_vs_zen))

	output_csv = 'log10(energy) [eV], deep veff*sr [km^3sr], deep aeff*sr [km^2sr], shallow veff*sr [km^3sr], shallow aeff*str [km^2sr]'
	output_csv += "\n"

	for iE, energy in enumerate(energies):
		output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e} \n'.format(np.log10(energy), deep_veff[iE], deep_aeff[iE], shallow_veff[iE], shallow_aeff[iE])

	with open(f'tabulated_veff_aeff_{deep_det}_{shallow_det}.csv', 'w') as fout:
		fout.write(output_csv)

	output_csv = 'czmin, deep aeff [km^2], shallow aeff [km^2]'
	output_csv += "\n"
	for iZ, _ in enumerate(deep_aeff_vs_zen):
		output_csv += '{:1f}, {:e}, {:e} \n'.format(np.cos(zen_bins[iZ][0]), deep_aeff_vs_zen[iZ], shallow_aeff_vs_zen[iZ])

	with open(f'tabulated_aeff_vs_zen_{deep_det}_{shallow_det}_Ebin_{which_e_bin}.csv', 'w') as fout:
		fout.write(output_csv)









