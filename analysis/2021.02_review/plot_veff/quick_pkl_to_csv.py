import numpy as np
import matplotlib.pyplot as plt
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
import pickle

n_deep = 143
n_shallow_infill = 130
n_shallow_coinc = 143
n_shallow = n_shallow_infill + n_shallow_coinc

flavors = ['e', 'mu', 'tau']

deep_veff = np.zeros(9)
deep_aeff = np.zeros(9)
shallow_veff = np.zeros(9)
shallow_aeff = np.zeros(9)
energies = np.zeros(9)

for iF, flavor in enumerate(flavors):
	filename = f'data/deep_only_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for i, key in enumerate(data.keys()): # assume all have the same number of energies
		energies[i] = np.power(10.,float(key))
		the_veff = data[key]['total_veff']/n_deep
		the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
		deep_veff[i] += the_veff * 4 * np.pi /units.km**3
		deep_aeff[i] += the_aeff * 4 * np.pi /units.km**2

for iF, flavor in enumerate(flavors):
	filename = f'data/shallow_only_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for i, key in enumerate(data.keys()): # assume all have the same number of energies
		the_veff = data[key]['total_veff']/n_shallow
		the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
		shallow_veff[i] += the_veff * 4 * np.pi /units.km**3
		shallow_aeff[i] += the_aeff * 4 * np.pi /units.km**2

deep_veff/=3
deep_aeff/=3
shallow_veff/=3
shallow_aeff/=3



output_csv = 'log10(energy) [eV], deep veff*sr [km^3sr], deep aeff*sr [km^2sr], shallow veff*sr [km^3sr], shallow aeff*str [km^2sr]\n'
for iE, energy in enumerate(energies):
	output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e} \n'.format(np.log10(energy), deep_veff[iE], deep_aeff[iE], shallow_veff[iE], shallow_aeff[iE])

with open(f'tabulated_veff_aeff_review_hybrid.csv', 'w') as fout:
		fout.write(output_csv)







