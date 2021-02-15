import numpy as np
import matplotlib.pyplot as plt
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
import pickle

n_deep = 143
n_shallow_infill = 130
n_shallow_coinc = 143
n_shallow = n_shallow_infill + n_shallow_coinc
deep_det = 'pa_200m_2.00km'
deep_trigger = 'PA_4channel_100Hz'
shallow_det = 'surface_4LPDA_PA_15m_RNOG_300K_1.00km'
shallow_trigger = 'LPDA_2of4_100Hz'

flavors = ['e', 'mu', 'tau']

# deep_veff = np.zeros(9)
# deep_aeff = np.zeros(9)
# shallow_veff = np.zeros(9)
# shallow_aeff = np.zeros(9)
# energies = np.zeros(9)

# for iF, flavor in enumerate(flavors):
# 	filename = f'results/deep_only_{flavor}.pkl'
# 	data = pickle.load(open(filename, 'br'))
# 	for i, key in enumerate(data.keys()): # assume all have the same number of energies
# 		energies[i] = np.power(10.,float(key))
# 		the_veff = data[key]['total_veff']/n_deep
# 		the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
# 		deep_veff[i] += the_veff * 4 * np.pi /units.km**3
# 		deep_aeff[i] += the_aeff * 4 * np.pi /units.km**2

# for iF, flavor in enumerate(flavors):
# 	filename = f'results/shallow_only_{flavor}.pkl'
# 	data = pickle.load(open(filename, 'br'))
# 	for i, key in enumerate(data.keys()): # assume all have the same number of energies
# 		the_veff = data[key]['total_veff']/n_shallow
# 		the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
# 		shallow_veff[i] += the_veff * 4 * np.pi /units.km**3
# 		shallow_aeff[i] += the_aeff * 4 * np.pi /units.km**2

# deep_veff/=3
# deep_aeff/=3
# shallow_veff/=3
# shallow_aeff/=3

# and now, we need to calculate the single station fractions
overlap_fractions = np.zeros(9)
for iF, flavor in enumerate(flavors):
	filename = f'results/overlap_{deep_det}_{deep_trigger}_{shallow_det}_{shallow_trigger}_{flavor}.pkl'
	data = pickle.load(open(filename), 'br')
	for k, key in enumerate(data.keys()):
		the_veff = data[key]['total_veff']
		the_veff_dual = data[key]['total_veff']




# output_csv = 'log10(energy) [eV], deep veff*sr [km^3sr], deep aeff*sr [km^2sr], shallow veff*sr [km^3sr], shallow aeff*str [km^2sr]\n'
# for iE, energy in enumerate(energies):
# 	output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e} \n'.format(np.log10(energy), deep_veff[iE], deep_aeff[iE], shallow_veff[iE], shallow_aeff[iE])

# with open(f'results/tabulated_veff_aeff_review_hybrid.csv', 'w') as fout:
# 		fout.write(output_csv)







