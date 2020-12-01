import numpy as np
import os

flavors = ["e", "mu", "tau"]

step1dir = "/data/sim/Gen2/radio/2020/simulation_input/secondaries_500km2/step1/"
step2dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2"

det_files_dict = {
	"gen2r_200m_2km" : "dipoles_RNOG_200m_2.00km",
	"gen2r_200m_3km" : "dipoles_RNOG_200m_3.00km",
	"gen2r_100m_2km" : "dipoles_RNOG_100m_2.00km",
	"gen2r_100m_3km" : "dipoles_RNOG_100m_3.00km",
	"gen2r_surf_1km" : "surface_4LPDA_1dipole_RNOG_1.00km",
	"gen2r_surf_15km" : "surface_4LPDA_1dipole_RNOG_1.50km",
	"gen2r_20m_1km" : "dipoles_RNOG_20m_1.00km"
}

#det_files_labels = ["gen2r_100m_3km", "gen2r_200m_3km", "gen2r_surf_15km"]
det_files_labels = ["gen2r_surf_1km", "gen2r_surf_15km"]
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole_250MHz"

for det_file_label in det_files_labels:
	for flavor in flavors:
		det_file = det_files_dict[det_file_label]

		# load the npz files containing the missing jobs
		redo_file='redo_list_'+det_file_label+'_'+flavor+'.npz'
		npzfile = np.load(redo_file)
		the_logEs = npzfile['energies']
		the_czmins = npzfile['czmins']
		the_czmaxs = npzfile['czmaxs']
		the_jobs = npzfile['jobs']

		# set up the new dag file
		dag_file_name='dagman_step2_v2_'+det_file_label+'_'+flavor+'.dag'
		instructions = ""
		instructions += 'CONFIG config.dagman\n'
		instructions += f'VARS ALL_NODES step1dir="{step1dir}" step2dir="{step2dir}" detfile="{det_file}" configfile="{config_file}" simfile="{sim_file}"\n\n'

		with open(dag_file_name, 'w') as f:
			f.write(instructions)

		master_index=0

		for i, the_logE in enumerate(the_logEs):

			instructions = ""
			instructions += f'JOB job_{master_index} step2_job.sub \n'
			instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{the_logEs[i]:.2f}" czmin="{the_czmins[i]:.1f}" czmax="{the_czmaxs[i]:.1f}" part="{the_jobs[i]:06}"\n\n'

			with open(dag_file_name, 'a') as f:
				f.write(instructions)

			master_index+=1
