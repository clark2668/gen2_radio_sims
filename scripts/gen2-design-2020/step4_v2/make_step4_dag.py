import numpy as np
from NuRadioReco.utilities import units
import helper as hp

flavors = ["e", "mu", "tau"]
# flavors = ["mu", "tau"]
flavors = ["mu"]

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

step3dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step3"

detsim_files_dict = {
	"pa_100m_2.00km" : "D05phased_array_deep",
	"pa_100m_3.00km" : "D05phased_array_deep",
	"pa_200m_2.00km" : "D05phased_array_deep",
	"pa_200m_3.00km" : "D05phased_array_deep",
	"surface_4LPDA_PA_15m_RNOG_300K_1.00km" : "D09surface_4LPDA_pa_15m_250MHz",
	"surface_4LPDA_PA_15m_RNOG_300K_1.50km" : "D09surface_4LPDA_pa_15m_250MHz"
}

det_files_dict = {
	"gen2r_100m_2km" : "pa_100m_2.00km",
	"gen2r_100m_3km" : "pa_100m_3.00km",
	"gen2r_200m_2km" : "pa_200m_2.00km",
	"gen2r_200m_3km" : "pa_200m_3.00km",
	"gen2r_surf_1km" : "surface_4LPDA_PA_15m_RNOG_300K_1.00km",
	"gen2r_surf_15km" : "surface_4LPDA_PA_15m_RNOG_300K_1.50km",
}


det_files_labels = ["gen2r_100m_2km", "gen2r_100m_3km", "gen2r_200m_2km", "gen2r_200m_3km", "gen2r_surf_1km", "gen2r_surf_15km"]
#det_files_labels = ["gen2r_surf_1km", "gen2r_surf_15km"]
config_file = "config_Alv2009_noise_100ns"


dag_file_name='dagman_step4_fix_0.1.dag'
instructions = ""
instructions += 'CONFIG config.dagman\n\n\n'
with open(dag_file_name, 'w') as f:
	f.write(instructions)

master_index=0

for det_file_label in det_files_labels:

	det_file = det_files_dict[det_file_label]
	sim_file = detsim_files_dict[det_file]

	for flavor in flavors:
		for iE in range(len(logEs)):
			for iC in range(len(coszenbins)-1):
				czen1 = coszenbins[iC]
				czen2 = coszenbins[iC+1]

				round_czen1 = round(czen1, 1)

				# to start, do the "easy" small ones in the upgoing region
				# if round_czen1 not in [round(-0.2, 1), round(0.3, 1), round(0.4, 1), round(0.5, 1)]:
				# if round_czen1 not in [round(-0.1, 1), round(0.0, 1), round(0.1, 1), round(0.2, 1)]:
				if round_czen1 not in [round(0.1, 1)]:					
					continue

				round_logE = round(logEs[iE], 1)
				if round_logE not in [round(19.5, 1)]:
					continue

				instructions = ""
				instructions += f'JOB job_{master_index} step4_job.sub \n'
				instructions += f'VARS job_{master_index} step3dir="{step3dir}/{det_file}/{config_file}/{sim_file}/" detlabel="{det_file_label}" flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" \n\n'

				with open(dag_file_name, 'a') as f:
					f.write(instructions)

				master_index+=1



