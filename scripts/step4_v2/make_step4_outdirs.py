import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

base_dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step4/"

detsim_files_dict = {
	"pa_100m_2.00km" : "D05phased_array_deep",
	"pa_100m_3.00km" : "D05phased_array_deep",
	"pa_200m_2.00km" : "D05phased_array_deep",
	"pa_200m_3.00km" : "D05phased_array_deep",
	"surface_4LPDA_PA_15m_RNOG_300K_1.00km" : "D09surface_4LPDA_pa_15m_250MHz",
	"surface_4LPDA_PA_15m_RNOG_300K_1.50km" : "D09surface_4LPDA_pa_15m_250MHz"
}

det_files = ['pa_100m_2.00km', 'pa_100m_3.00km', 'pa_200m_2.00km', 'pa_200m_3.00km', 'surface_4LPDA_PA_15m_RNOG_300K_1.00km', 'surface_4LPDA_PA_15m_RNOG_300K_1.50km']
config_file = "config_Alv2009_noise_100ns"

for det_file in det_files:
	sim_file = detsim_files_dict[det_file]
	step4dir = os.path.join(base_dir, f"{det_file}", f"{config_file}", f"{sim_file}")
	if(not os.path.exists(step4dir)):
		os.makedirs(step4dir)

	coszenbins = hp.get_coszenbins()
	logEs = hp.get_logEs()
	energies = 10 ** logEs * units.eV

	flavors = ["e", "mu", "tau"]

	for flavor in flavors:
		folder = os.path.join(step4dir, flavor)
		if(not os.path.exists(folder)):
			os.makedirs(folder)
