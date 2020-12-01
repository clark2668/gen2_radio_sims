import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

base_dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step3/"

detsim_files_dict = {
	"dipoles_RNOG_200m_2.00km" : "D05phased_array_deep",
	"dipoles_RNOG_200m_3.00km" : "D05phased_array_deep",
	"dipoles_RNOG_100m_2.00km" : "D05phased_array_deep",
	"dipoles_RNOG_100m_3.00km" : "D05phased_array_deep",
	"surface_4LPDA_1dipole_RNOG_1.00km" : "D07surface_4LPDA_pa_15m_250MHz.py",
	"surface_4LPDA_1dipole_RNOG_1.50km" : "D07surface_4LPDA_pa_15m_250MHz.py"
}

det_files = ['dipoles_RNOG_200m_2.00km', 'dipoles_RNOG_200m_3.00km', 'dipoles_RNOG_100m_2.00km', 'dipoles_RNOG_100m_3.00km', 'surface_4LPDA_1dipole_RNOG_1.00km', 'surface_4LPDA_1dipole_RNOG_1.50km']
config_file = "config_Alv2009_noise_100ns"

for det_file in det_files:
	sim_file = detsim_files_dict[det_file]
	step3dir = os.path.join(base_dir, f"{det_file}", f"{config_file}", f"{sim_file}")
	if(not os.path.exists(step3dir)):
		os.makedirs(step3dir)

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
				folder = os.path.join(step3dir, flavor, f"{pattern}")
				if(not os.path.exists(folder)):
					os.makedirs(folder)
