flavors = ["e", "mu", "tau"]
flavors = ["e"]

step2dir = "/data/user/brianclark/Gen2/simulation_output/secondaries_500km2"

det_files = ["dipoles_RNOG_200m_2.00km", "dipoles_RNOG_20m_1.00km"]
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole_250MHz"


dag_file_name='dagman_step3.dag'
instructions = ""
instructions += 'CONFIG config.dagman\n'
with open(dag_file_name, 'w') as f:
	f.write(instructions)

master_index=0
for det_file in det_files:

	for flavor in flavors:

		instructions = ""
		instructions += f'JOB job_{master_index} step3_job.sub \n'
		instructions += f'VARS job_{master_index} flavor="{flavor}" step2dir="{step2dir}/{det_file}/{config_file}/{sim_file}/"\n\n'

		with open(dag_file_name, 'a') as f:
			f.write(instructions)

		master_index+=1
