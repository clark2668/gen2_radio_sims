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
flavor = 'mu'

combo = trigger1 + "_" + trigger2

result = {}
result[combo] = {'E' : [],
					'c': []}

pkl_file_name = station1 + "_" + trigger1 + "_" + station2 + "_" + trigger2 + "_" + flavor + ".pkl"
with open(pkl_file_name, "rb") as fin:
	coincidences = pickle.load(fin)

	for lgE, value in coincidences.items():
		result[combo]['E'].append(lgE)
		print(f"E = 10^{lgE}eV")

		n_stations = np.array(value[combo])
		n_tot = np.sum(n_stations>0)
		n_stations1 = np.array(coincidences[lgE]["1"][trigger1])
		n_stations2 = np.array(coincidences[lgE]["2"][trigger2])

		weights = np.array(coincidences[lgE]['weights'])
		weights_dual = np.sum(weights[(n_stations1>=1) & (n_stations2>=1)])
		weights_total = np.sum(weights[n_stations>0])
		fraction_dual = weights_dual/weights_total
		print("Fraction of dual events is {:.4f}/{:.4f} = {:e}".format(weights_dual, weights_total, fraction_dual))

		result[combo]['c'].append(fraction_dual)


fig, ax = plt.subplots(1, 1)
title = "at least 1 [200m deep 4ch PA] and 1 [surface 2/4 LPDA]) nu_{}".format(flavor)
xx = result[combo]['E']
ax.plot(xx, result[combo]['c'], 'o')
ax.set_title(title)
ax.set_ylim(0, 1)
ax.set_xlabel("log10(energy [eV])")
ax.set_ylabel("coincidence rate")
ax.legend()
# fig.tight_layout()
fig.savefig('coincidences_{}.png'.format(flavor))
