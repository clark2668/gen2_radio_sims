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
from NuRadioReco.detector import detector
from NuRadioMC.utilities import fluxes
from NuRadioMC.utilities.Veff import get_Veff_Aeff, get_Veff_Aeff_array, get_index, get_Veff_water_equivalent
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
plt.switch_backend('agg')

if __name__ == "__main__":

	# reopen the saved npz file
	npzfile = np.load('veffs_200m.npz')
	Veffs = npzfile['Veffs']
	energies = npzfile['energies']
	energies_low = npzfile['energies_low']
	energies_up = npzfile['energies_up']
	zenith_bins = npzfile['zenith_bins']
	utrigger_names = npzfile['utrigger_names']

	# calculate the average over all zenith angle bins (in this case only one bin that contains the full sky)
	Veff = np.average(Veffs[:, :, get_index("dipole_1.0sigma", utrigger_names), 0], axis=1)
	# we also want the water equivalent effective volume times 4pi
	Veff = get_Veff_water_equivalent(Veff) * 4 * np.pi
	# calculate the uncertainty for the average over all zenith angle bins. The error relative error is just 1./sqrt(N)
	Veff_error = Veff / np.sum(Veffs[:, :, get_index("dipole_1.0sigma", utrigger_names), 2], axis=1) ** 0.5
	# plot effective volume
	fig, ax = plt.subplots(1, 1, figsize=(6, 6))
	ax.errorbar(energies / units.eV, Veff / units.km ** 3 / units.sr,
				yerr=Veff_error / units.km ** 3 / units.sr, fmt='d-')
	ax.semilogx(True)
	ax.semilogy(True)
	ax.set_xlabel("neutrino energy [eV]")
	ax.set_ylabel("effective volume [km$^3$ sr]")
	# ax.set_ylim([1e3,3e3])
	fig.tight_layout()
	fig.savefig("Veff.png")

	# plot expected limit
	fig, ax = limits.get_E2_limit_figure(diffuse=True, show_grand_10k=True, show_grand_200k=False)
	labels = []
	labels = limits.add_limit(ax, labels, energies, Veff,
							  n_stations=1, label='200m', livetime=10 * units.year, linestyle='-', color='blue', linewidth=3)
	leg = plt.legend(handles=labels, loc=2)
	fig.savefig("limits.png")
	plt.show()