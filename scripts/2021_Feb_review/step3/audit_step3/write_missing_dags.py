import numpy as np
import os

#flavors = ["e", "mu", "tau"]
# flavors = ["mu", "tau"]
flavors = ["mu"]

step2dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step2"
step3dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step3"

step2_step3_dict = {
	"pa_100m_2.00km" : "dipoles_RNOG_100m_2.00km",
	"pa_100m_3.00km" : "dipoles_RNOG_100m_3.00km",
	"pa_200m_2.00km" : "dipoles_RNOG_200m_2.00km",
	"pa_200m_3.00km" : "dipoles_RNOG_200m_3.00km",
	"surface_4LPDA_PA_15m_RNOG_300K_1.00km" : "surface_4LPDA_1dipole_RNOG_1.00km",
	"surface_4LPDA_PA_15m_RNOG_300K_1.50km" : "surface_4LPDA_1dipole_RNOG_1.50km"
}

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
#det_files_labels = ["gen2r_surf_1km"]
config_file = "config_Alv2009_noise_100ns"

for det_file_label in det_files_labels:
	
	det_file = det_files_dict[det_file_label]
	sim_file = detsim_files_dict[det_file]
	step2_detfile = step2_step3_dict[det_file]

	for flavor in flavors:

		# load the npz files containing the missing jobs
		redo_file='redo_list_step3_'+det_file_label+'_'+flavor+'.npz'
		npzfile = np.load(redo_file)
		the_logEs = npzfile['energies']
		the_czmins = npzfile['czmins']
		the_czmaxs = npzfile['czmaxs']
		the_jobs = npzfile['jobs']

		# set up the new dag file
		dag_file_name='dagman_step3_v2_'+det_file_label+'_'+flavor+'.dag'
		instructions = ""
		instructions += 'CONFIG config.dagman\n'
		instructions += f'VARS ALL_NODES step2dir="{step2dir}" step3dir="{step3dir}" step2detfile="{step2_detfile}" detfile="{det_file}" configfile="{config_file}" simfile="{sim_file}"\n\n'

		with open(dag_file_name, 'w') as f:
			f.write(instructions)

		master_index=0

		for i, the_logE in enumerate(the_logEs):

			instructions = ""
			instructions += f'JOB job_{master_index} step3_job.sub \n'
			instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{the_logEs[i]:.2f}" czmin="{the_czmins[i]:.1f}" czmax="{the_czmaxs[i]:.1f}" part="{the_jobs[i]:06}"\n\n'


			with open(dag_file_name, 'a') as f:
				f.write(instructions)

			master_index+=1
