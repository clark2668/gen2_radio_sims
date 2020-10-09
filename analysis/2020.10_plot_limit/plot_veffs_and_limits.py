import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
from scipy import interpolate
import json
import os
import sys

from NuRadioReco.utilities import units
from NuRadioMC.utilities import fluxes
from NuRadioMC.utilities.Veff import get_Veff_Aeff, get_Veff_Aeff_array, get_index, get_Veff_water_equivalent
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
# plt.switch_backend('agg')

class veff_info:
	pass

def load_veff_info(depth):
	holder = veff_info()
	npzfile = np.load('veffs_'+depth+'m.npz')
	holder.Veffs = npzfile['Veffs']
	holder.energies = npzfile['energies']
	holder.energies_low = npzfile['energies_low']
	holder.energies_up = npzfile['energies_up']
	holder.zenith_bins = npzfile['zenith_bins']
	holder.utrigger_names = npzfile['utrigger_names']
	return holder


if __name__ == "__main__":

	depths=['200', '20']
	data_holders = {}
	for i, depth in enumerate(depths):
		data_holders[depth] = load_veff_info(depth)


	# plot for veff
	fig_veff = plt.figure(figsize=(11,8))
	ax_veff = fig_veff.add_subplot(111)

	fig_veff_vs_dec = plt.figure(figsize=(11,8))
	ax_veff_vs_dec = fig_veff_vs_dec.add_subplot(111)

	# as well as for limit
	fig_limit, ax_limit = limits.get_E2_limit_figure(diffuse=True, show_grand_10k=False, show_grand_200k=False)
	labels = []

	colors = ['blue', 'orange']

	for iD, depth in enumerate(depths):
		# calculate the average over all zenith angle bins (in this case only one bin that contains the full sky)
		Veff = np.average(data_holders[depth].Veffs[:, :, get_index("dipole_1.0sigma", data_holders[depth].utrigger_names), 0], axis=1)
		# we also want the water equivalent effective volume times 4pi
		Veff = get_Veff_water_equivalent(Veff) * 4 * np.pi
		# calculate the uncertainty for the average over all zenith angle bins. The error relative error is just 1./sqrt(N)
		Veff_error = Veff / np.sum(data_holders[depth].Veffs[:, :, get_index("dipole_1.0sigma", data_holders[depth].utrigger_names), 2], axis=1) ** 0.5
		# plot effective volume
	
		ax_veff.errorbar(data_holders[depth].energies / units.eV, Veff / units.km ** 3 / units.sr,
			yerr=Veff_error / units.km ** 3 / units.sr, fmt='o-', color=colors[iD], linewidth=3, label=depth+'m')

		labels = limits.add_limit(ax_limit, labels, data_holders[depth].energies, Veff,
			n_stations=1, label=depth+'m', livetime=10 * units.year, linestyle='-', color=colors[iD], linewidth=3)

		# and declination band scan
		if iD<1:
			for iE in range(len(data_holders[depth].energies)):
				banded_veff = []
				banded_veff_err = []
				for band in range(20):
					this_veff = data_holders[depth].Veffs[iE,band,get_index("dipole_1.0sigma", data_holders[depth].utrigger_names),0]
					this_veff = get_Veff_water_equivalent(this_veff)
					this_veff_err = this_veff / np.sum(data_holders[depth].Veffs[iE,band,get_index("dipole_1.0sigma", data_holders[depth].utrigger_names), 2]) ** 0.5
					banded_veff.append(this_veff)
					banded_veff_err.append(this_veff_err)
				banded_veff = np.asarray(banded_veff)
				banded_veff_err = np.asarray(banded_veff_err)
				# nb, zenith_bins is 2D array oc czmins and czmaxs, so wen eed to slice against it
				ax_veff_vs_dec.plot(np.cos(data_holders[depth].zenith_bins[:,0]), 
					banded_veff/units.km ** 3, 
					# yerr = banded_veff_err/units.km ** 3,
					label=np.log10(data_holders[depth].energies[iE]),
					linewidth=2)

	# plot the veffs
	ax_veff.set_yscale('log')
	ax_veff.set_xscale('log')
	ax_veff.set_xlabel("neutrino energy [eV]",size=20)
	ax_veff.set_ylabel("effective volume [km$^3$ sr]",size=20)
	ax_veff.tick_params(labelsize=20)
	ax_veff.legend(fontsize=20)
	fig_veff.savefig("veff.png",edgecolor='none', bbox_inches='tight')

	ax_veff_vs_dec.set_yscale('log')
	# ax_veff_vs_dec.set_xscale('log')
	ax_veff_vs_dec.set_xlabel(r'cos($\theta$)',size=20)
	ax_veff_vs_dec.set_ylabel("effective volume [km$^3$]",size=20)
	ax_veff_vs_dec.tick_params(labelsize=20)
	ax_veff_vs_dec.legend(fontsize=20)
	ax_veff_vs_dec.set_ylim([10,3e3])
	ax_veff_vs_dec.set_xlim([-0.25,1.1])
	fig_veff_vs_dec.savefig("veff_vs_dec.png",edgecolor='none', bbox_inches='tight')


	# plot expected limit
	leg = plt.legend(handles=labels, loc=2)
	fig_limit.savefig("limits.png")
