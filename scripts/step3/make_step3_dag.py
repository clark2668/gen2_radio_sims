flavors = ["e", "mu", "tau"]

step2dir = "/data/user/brianclark/Gen2/simulation_output/secondaries_500km2"

det_file = "dipoles_100m"
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole"


dag_file_name='dagman_step3.dag'
instructions = ""
instructions += 'CONFIG config.dagman\n'
instructions += f'VARS ALL_NODES step2dir="{step2dir}/{det_file}/{config_file}/{sim_file}/"\n\n'
with open(dag_file_name, 'w') as f:
	f.write(instructions)

master_index=0
for flavor in flavors:

	instructions = ""
	instructions += f'JOB job_{master_index} step3_job.sub \n'
	instructions += f'VARS job_{master_index} flavor="{flavor}" \n\n'

	with open(dag_file_name, 'a') as f:
		f.write(instructions)

	master_index+=1
