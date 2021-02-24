import numpy as np
import matplotlib.pyplot as plt
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
import pickle

n_deep = 143
n_shallow_infill = 130
n_shallow_coinc = 143 
n_shallow = n_shallow_infill + n_shallow_coinc
# det = 'deep_only_100m'
det = 'shallow_only'
n_to_divide = 1
if 'deep' in det:
	n_to_divide = n_deep
if 'shallow' in det:
	n_to_divide = n_shallow

flavors = ['e', 'mu', 'tau']

# but, we also need the veff per zenith band at at given energy
aeff_vzen = np.zeros((9,20))
energies = np.zeros(9)
zen_bins = None

for iF, flavor in enumerate(flavors):
	filename = f'results/{det}_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for i, key in enumerate(data.keys()): # assume all have the same number of energies
		energies[i] = np.power(10.,float(key))
		the_veff = data[key]['total_veff']/n_to_divide
		# the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
		# deep_veff[i] += the_veff * 4 * np.pi /units.km**3
		# deep_aeff[i] += the_aeff * 4 * np.pi /units.km**2'
		if zen_bins is None:
			zen_bins = data[key]['czmins']

		for iz in range(20):
			the_veff_zbin = data[key]['total_veff_zen_bins'][iz]/n_to_divide
			the_aeff_zbin = the_veff_zbin / cross_sections.get_interaction_length(np.power(10., float(key)))
			aeff_vzen[i][iz] += the_aeff_zbin/units.km**2

aeff_vzen/=3

filename = f'{det}_skycoverage.npz'
np.savez(filename, energies=energies, zen_bins=zen_bins, aeff_vzen = aeff_vzen)




