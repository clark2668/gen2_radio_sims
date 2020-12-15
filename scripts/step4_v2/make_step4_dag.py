import numpy as np
from NuRadioReco.utilities import units
import helper as hp

flavors = ["e", "mu", "tau"]

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

step3dir = "/data/user/brianclark/Gen2/simulation_output/secondaries_500km2/step3/"

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
det_files_labels = ["gen2r_surf_15km"] ## REMOVE
config_file = "config_Alv2009_noise_100ns"
# config_file = "config_Alv2009_nonoise_100ns" ## REMOVE

dag_file_name='dagman_step4.dag'
instructions = ""
instructions += 'CONFIG config.dagman\n'
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

				if logEs[iE]>18.5: #REMOVE
					continue #REMOVE
				if czen1 < 0.0:
					continue
				if czen1 > 0.1:
					continue

				instructions = ""
				instructions += f'JOB job_{master_index} step4_job.sub \n'
				instructions += f'VARS job_{master_index} step3dir="{step3dir}/{det_file}/{config_file}/{sim_file}/" flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" \n\n'

				with open(dag_file_name, 'a') as f:
					f.write(instructions)

				master_index+=1



