import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

flavors = ["e", "mu", "tau"]
flavors = ["e"]


step2dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step2"
step3dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step3"

step2_step3_dict = {
	"pa_100m_2.00km" : "dipoles_RNOG_100m_2.00km",
	"pa_100m_3.00km" : "dipoles_RNOG_100m_3.00km",
	"pa_200m_2.00km" : "dipoles_RNOG_200m_2.00km",
	"pa_200m_3.00km" : "dipoles_RNOG_200m_3.00km",
	"surface_4LPDA_PA_15m_RNOG_1.00km" : "surface_4LPDA_1dipole_RNOG_1.00km",
	"surface_4LPDA_PA_15m_RNOG_1.50km" : "surface_4LPDA_1dipole_RNOG_1.50km"
}

detsim_files_dict = {
	"pa_100m_2.00km" : "D05phased_array_deep",
	"pa_100m_3.00km" : "D05phased_array_deep",
	"pa_200m_2.00km" : "D05phased_array_deep",
	"pa_200m_3.00km" : "D05phased_array_deep",
	"surface_4LPDA_PA_15m_RNOG_1.00km" : "D07surface_4LPDA_pa_15m_250MHz.py",
	"surface_4LPDA_PA_15m_RNOG_1.50km" : "D07surface_4LPDA_pa_15m_250MHz.py"
}

det_files_dict = {
	"gen2r_100m_2km" : "pa_100m_2.00km",
	"gen2r_100m_3km" : "pa_100m_3.00km",
	"gen2r_200m_2km" : "pa_200m_2.00km",
	"gen2r_200m_3km" : "pa_200m_3.00km",
	"gen2r_surf_1km" : "surface_4LPDA_PA_15m_RNOG_1.00km",
	"gen2r_surf_15km" : "surface_4LPDA_PA_15m_RNOG_1.50km",
}


det_files_labels = ["gen2r_200m_3km"]
config_file = "config_Alv2009_noise_100ns"

for det_file_label in det_files_labels:
	
	det_file = det_files_dict[det_file_label]
	sim_file = detsim_files_dict[det_file]
	step2_detfile = step2_step3_dict[det_file]
	
	for flavor in flavors:
		dag_file_name='dagman_step3_'+det_file_label+'_'+flavor+'.dag'
		instructions = ""
		instructions += 'CONFIG config.dagman\n'
		instructions += f'VARS ALL_NODES step2dir="{step2dir}" step3dir="{step3dir}" step2detfile="{step2_detfile}" detfile="{det_file}" configfile="{config_file}" simfile="{sim_file}"\n\n'
		with open(dag_file_name, 'w') as f:
			f.write(instructions)

		master_index=0

		for iE in range(len(logEs)):

			for iC in range(len(coszenbins)-1):
				czen1 = coszenbins[iC]
				czen2 = coszenbins[iC + 1]
				E = energies[iE]

				num_parts, num_events = hp.get_number_of_parts_and_events(flavor, logEs[iE], czen1)
				
				for ijob in range(num_parts):
					instructions = ""
					instructions += f'JOB job_{master_index} step3_job.sub \n'
					instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" part="{ijob:06}"\n\n'

					with open(dag_file_name, 'a') as f:
						f.write(instructions)

					master_index+=1

