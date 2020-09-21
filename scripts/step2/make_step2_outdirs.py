import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

base_dir = "/data/user/brianclark/Gen2/simulation_output/"

det_file = "dipoles_100m"
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole"

step2dir = os.path.join(base_dir, f"secondaries_500km2", f"{det_file}", f"{config_file}", f"{sim_file}")
if(not os.path.exists(step2dir)):
	os.makedirs(step2dir)

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

flavors = ["e", "mu", "tau"]

for flavor in flavors:
	for iE in range(len(logEs)):
		for iC in range(len(coszenbins) - 1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			E = energies[iE]
			pattern = f"{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}"
			print(pattern)
			folder = os.path.join(step2dir, flavor, f"{pattern}")
			if(not os.path.exists(folder)):
				os.makedirs(folder)