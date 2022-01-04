import numpy as np
from NuRadioReco.utilities import units
import helper as hp

# flavors = ["mu", "tau"]
flavors = ["mu"]

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

step1dir = "/data/user/brianclark/Gen2/simulation_input/secondaries_500km2/step1"

dag_file_name='dagman_tarstep1.dag'
instructions = ""
instructions += 'CONFIG config.dagman\n'
with open(dag_file_name, 'w') as f:
	f.write(instructions)

master_index=0
for flavor in flavors:
	for iE in range(len(logEs)):
		for iC in range(len(coszenbins)-1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC+1]
			instructions = ""
			instructions += f'JOB job_{master_index} tar_step1_job.sub \n'
			instructions += f'VARS job_{master_index} step1dir="{step1dir}/" flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" \n\n'

			with open(dag_file_name, 'a') as f:
				f.write(instructions)

			master_index+=1



