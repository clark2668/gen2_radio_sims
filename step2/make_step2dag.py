import numpy as np
import os

from NuRadioReco.utilities import units

coszenbins = np.linspace(-1, 1, 21)
logEs = np.arange(15., 20.1, 0.5)
energies = 10 ** logEs * units.eV

n_parts = 2
n_parts_per_file = np.ones(len(coszenbins)-1, dtype=np.int) * 1
flavors = ["e", "mu", "tau"]

step1dir = "/data/user/brianclark/Gen2/simulation_input/secondaries_500km2/step1/"
step2dir = "/data/user/brianclark/Gen2/simulation_output/secondaries_500km2"

det_file = "dipoles_100m"
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole"

dag_file_name='dagman_step2.dag'

# write the master variables
instructions = ""
instructions += 'CONFIG config.dagman\n'
instructions += f'VARS ALL_NODES step1dir="{step1dir}" step2dir="{step2dir}" detfile="{det_file}" configfile="{config_file}" simfile="{sim_file}"\n\n'
with open(dag_file_name, 'w') as f:
	f.write(instructions)

master_index=0
for flavor in flavors:
	for iE in range(len(logEs)):
		#if(logEs[iE]<20.0):
		#	continue

		for iC in range(len(coszenbins)-1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			if(czen2 > .3 or czen1 < -0.3):
				continue
			E = energies[iE]
			
			for ijob in range(n_parts//n_parts_per_file[iC]):
				for ipart in range(ijob * n_parts_per_file[iC], (ijob + 1) * n_parts_per_file[iC]):
					instructions = ""
					instructions += f'JOB job_{master_index} step2_job.sub \n'
					instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" part="{ipart:06}"\n\n'

					with open(dag_file_name, 'a') as f:
						f.write(instructions)

					master_index+=1

