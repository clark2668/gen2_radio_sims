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

deep_veff = np.zeros(9)
deep_aeff = np.zeros(9)
shallow_veff = np.zeros(9)
shallow_aeff = np.zeros(9)
energies = np.zeros(9)

for iF, flavor in enumerate(flavors):
	filename = f'results/deep_only_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for i, key in enumerate(data.keys()): # assume all have the same number of energies
		energies[i] = np.power(10.,float(key))
		the_veff = data[key]['total_veff']/n_deep
		the_aeff = the_veff / cross_sections.get_interaction_length(np.power(10., float(key)))
		deep_veff[i] += the_veff * 4 * np.pi /units.km**3
		deep_aeff[i] += the_aeff * 4 * np.pi /units.km**2

for iF, flavor in enumerate(flavors):
	filename = f'results/shallow_only_{flavor}.pkl'
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

# and now, we need to calculate the single station fractions
overlap_fractions = np.zeros(9)
deep_only_fraction = np.zeros(9)
shallow_only_fraction = np.zeros(9)
for iF, flavor in enumerate(flavors):
	filename = f'results/overlap_{deep_det}_{deep_trigger}_{shallow_det}_{shallow_trigger}_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for k, key in enumerate(data.keys()):
		the_veff = data[key]['total_veff']
		the_veff_dual = data[key]['dual_veff']
		the_veff_deep = data[key]['deep_only_veff']
		the_veff_shallow = data[key]['shallow_only_veff']
		fraction = the_veff_dual/the_veff
		overlap_fractions[k] += fraction
		deep_only_fraction[k] += the_veff_deep/the_veff
		shallow_only_fraction[k] += the_veff_shallow/the_veff

overlap_fractions/=3
deep_only_fraction/=3
shallow_only_fraction/=3

output_csv = 'NB (!!): The overlap fraction is the fraction of events which overlap between the shallow and deep detectors when they are deployed at a ratio of 1:1.9\n'
output_csv += 'This is reasonably close to the 1:2.17 ratio in the review array, but is not exact.\n'
output_csv += 'So, to get the total array effective volume, you should do ((n_deep * deep_veff) + (n_shallow * shallow_veff))*(1-overlap_fraction)\n'
output_csv += 'But you should not trust that formula for n_deep == n_shallow, because that is NOT what was simulated. It needs to be ~1:2\n'
output_csv += "------\n"
output_csv += 'log10(energy) [eV], deep veff*sr [km^3sr], deep aeff*sr [km^2sr], shallow veff*sr [km^3sr], shallow aeff*str [km^2sr], overlap fraction, deep only fraction, shallow only fraction\n'
for iE, energy in enumerate(energies):
	output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e}, {:.3f}, {:.3f}, {:.3f} \n'.format(np.log10(energy), 
		deep_veff[iE], deep_aeff[iE], shallow_veff[iE], shallow_aeff[iE],
		overlap_fractions[iE], deep_only_fraction[iE], shallow_only_fraction[iE])

with open(f'results/tabulated_veff_aeff_review_hybrid.csv', 'w') as fout:
		fout.write(output_csv)







