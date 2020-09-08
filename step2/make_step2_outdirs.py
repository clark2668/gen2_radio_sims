import numpy as np
import os

from NuRadioReco.utilities import units

base_dir = "/data/user/brianclark/Gen2/simulation_output/"

det_file = dipoles_100m
config_file = config_Alv2009_nonoise_100ns
sim_file = D02single_dipole

step2dir = os.path.join(base_dir, f"secondaries_500km2", f"{detector_file}", f"{configuration_file}", f"{sim_file}")
if(not os.path.exists(step2dir)):
	os.makedirs(step2dir)

coszenbins = np.linspace(-1, 1, 21)
logEs = np.arange(15., 20.1, 0.5)
energies = 10 ** logEs * units.eV

n_parts = 2

n_parts_per_file = np.ones(len(coszenbins)-1, dtype=np.int) * 1

flavors = ["e", "mu", "tau"]

for flavor in flavors:
	for iE in range(len(logEs)):
		if(logEs[iE]<20.0):
			continue

		for iC in range(len(coszenbins) - 1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			if(czen2 > .3 or czen1 < -0.3):
				continue
			E = energies[iE]
			pattern = f"{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}"
			print(pattern)
			folder = os.path.join(step2dir, flavor, f"{pattern}")
			if(not os.path.exists(folder)):
				os.makedirs(folder)

			for ijob in range(n_parts//n_parts_per_file[iC]):
						
				if(not os.path.exists(os.path.join(step2dir, flavor, pattern))):
					os.makedirs(os.path.join(step2dir, flavor, pattern))
