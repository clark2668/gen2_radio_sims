import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
import json
import os
import sys
import pickle

station1 = 'pa_200m_2.00km'
station2 = 'surface_4LPDA_PA_15m_RNOG_300K_1.00km'
trigger1 = 'PA_4channel_100Hz'
trigger2 = 'LPDA_2of4_100Hz'

flavors = ['e', 'mu', 'tau']
result = {}
for flavor in flavors:
	result[flavor] = {'E' : [],
					'c_deep': [],
					'c_shallow': []}

	pkl_file_name = 'coinc_' + station1 + "_" + trigger1 + "_" + station2 + "_" + trigger2 + "_" + flavor + ".pkl"
	with open(pkl_file_name, "rb") as fin:
		coincidences = pickle.load(fin)

		for lgE, value in coincidences.items():
			result[flavor]['E'].append(lgE)
			result[flavor]['c_deep'].append(value['overlap_weight']/value['deep_weight'])
			result[flavor]['c_shallow'].append(value['overlap_weight']/value['shallow_weight'])

energies = result['e']['E']
average_deep = np.zeros(9)
average_shallow = np.zeros(9)
for iflavor, flavor in enumerate(flavors):
	for iE, energy in enumerate(energies):
		average_deep[iE]+=result[flavor]['c_deep'][iE]
		average_shallow[iE]+=result[flavor]['c_shallow'][iE]

output_csv = 'log10(energy) [eV], frac_deep_seen_in_shallow, frac_shallow_seen_in_deep'
output_csv += "\n"

for iE, energy in enumerate(energies):
	output_csv += '{:.1f}, {:.2f}, {:.2f} \n'.format(float(energy), average_deep[iE]/3, average_shallow[iE]/3)

with open(f'coinc_{station1}_{station2}.csv', 'w') as fout:
	fout.write(output_csv)



colors = ['C0', 'C1', 'C2']

fig, ax = plt.subplots(1, 1)
# title = "at least 1 [200m deep 4ch PA] and 1 [surface 2/4 LPDA]) nu_{}".format(flavor)
for iflavor, flavor in enumerate(flavors):
	xx = result[flavor]['E']
	ax.plot(xx, result[flavor]['c_deep'], 'o-', color=colors[iflavor], label='frac deep seen in shallow, {}'.format(flavor))
	ax.plot(xx, result[flavor]['c_shallow'], '^--', color=colors[iflavor], label='frac shallow seen in deep, {}'.format(flavor))
# ax.set_title(title)
ax.set_ylim(0, 1)
ax.set_xlabel("log10(energy [eV])")
ax.set_ylabel("coincidence rate")
ax.legend()
fig.tight_layout()
fig.savefig('matching_coincidences.png')
