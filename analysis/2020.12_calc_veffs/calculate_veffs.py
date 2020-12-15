import numpy as np
import sys

from NuRadioMC.utilities.Veff import get_Veff_Aeff, get_Veff_Aeff_array

if __name__ == "__main__":

	# depth = ''
	# if(len(sys.argv) == 1):
	# 	print("no depth specified!")
	# 	sys.exit()
	# else:
	# 	depth = sys.argv[1]

	top_dir='/data/user/brianclark/Gen2/test_out/noise'
	data = get_Veff_Aeff(top_dir, n_cores=1)
	Veffs, energies, energies_low, energies_up, zenith_bins, utrigger_names = get_Veff_Aeff_array(data)
	np.savez('veffs_noise.npz',Veffs=Veffs, energies=energies, energies_low=energies_low, energies_up=energies_up, zenith_bins=zenith_bins, utrigger_names=utrigger_names)
