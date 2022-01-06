import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

flavors = [
	"e", 
	# "mu", 
	# "tau"
	]

step0dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_input/secondaries_1700km2/step0/"
step1dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_input/secondaries_1700km2/step1/"

for flavor in flavors:
	
	dag_file_name='dagman_step1_'+flavor+'.dag'
	instructions = ""
	instructions += 'CONFIG config.dagman\n'
	instructions += f'VARS ALL_NODES step0dir="{step0dir}" step1dir="{step1dir}"\n\n'
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
				instructions += f'JOB job_{master_index} step1_job.sub \n'
				instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" part="{ijob:06}"\n\n'

				with open(dag_file_name, 'a') as f:
					f.write(instructions)

				master_index+=1

