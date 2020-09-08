import numpy as np
import os

from NuRadioReco.utilities import units

# base_dir = "/data/user/brianclark/Gen2/simulation_input/"

coszenbins = np.linspace(-1, 1, 21)
logEs = np.arange(15., 20.1, 0.5)
energies = 10 ** logEs * units.eV

n_parts = 2
n_parts_per_file = np.ones(len(coszenbins)-1, dtype=np.int) * 1
flavors = ["e", "mu", "tau"]

step0dir = "/data/user/brianclark/Gen2/simulation_input/secondaries_500km2/step0/"
step1dir = "/data/user/brianclark/Gen2/simulation_input/secondaries_500km2/step1/"

# write the master variables
instructions = ""
instructions += 'CONFIG dagman.config\n'
instructions += f'VAR ALL_NODES step0dir="{step0dir}" step1dir="{step1dir}"\n\n'
with open('step1_dagman.dag', 'w') as f:
	f.write(instructions)

master_index=0
for flavor in flavors:
	for iE in range(len(logEs)):
		if(logEs[iE]<20.0):
			continue

		for iC in range(len(coszenbins)-1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			if(czen2 > .3 or czen1 < -0.3):
				continue
			E = energies[iE]
			
			for ijob in range(n_parts//n_parts_per_file[iC]):
				for ipart in range(ijob * n_parts_per_file[iC], (ijob + 1) * n_parts_per_file[iC]):
					instructions = ""
					instructions += f'JOB job_{master_index} step1_job.sub \n'
					instructions += f'VARS job_{master_index} flavor="{flavor}" energy="{logEs[iE]:.2f}" czmin="{czen1:.1f}" czmax="{czen2:.1f}" part="{ipart:06}"\n\n'

					with open('step1_dagman.dag', 'a') as f:
						f.write(instructions)

					master_index+=1

