import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

flavors = [
			"e", 
			"mu", 
			"tau"
			]

step1dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_input/secondaries_1700km2/step1/"
step2dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step2/"

det_files_dict = {
	"gen2r_baseline" : "baseline_array",
	"gen2r_hybrid" : "hex_hybrid_only_array",
	"gen2r_shallow" : "hex_shallow_array",
	"gen2r_shallowheavy" : "hex_shallowheavy_array",
}
det_files_labels = [
	"gen2r_baseline", 
	"gen2r_hybrid" , 
	# "gen2r_shallow", 
	# "gen2r_shallowheavy"
	]
config_file = "config_ARZ2020_noise"
sim_file = "D01detector_sim"

for det_file_label in det_files_labels:
	for flavor in flavors:

		det_file = det_files_dict[det_file_label]
		dag_file_name='dagman_step2_'+det_file_label+'_'+flavor+'.dag'
		instructions = ""
		instructions += 'CONFIG config.dagman\n'
		instructions += f'VARS ALL_NODES step1dir="{step1dir}" step2dir="{step2dir}" detfile="{det_file}" configfile="{config_file}" simfile="{sim_file}"\n\n'
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
					instructions += f'JOB job_{master_index} step2_job.sub \n'
					instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" part="{ijob:06}"\n\n'

					with open(dag_file_name, 'a') as f:
						f.write(instructions)

					master_index+=1

