import numpy as np
import os

import helper as hp

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs

flavors = ["e", "mu", "tau"]

step2dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step2"

det_files_dict = {
	"gen2r_200m_2km" : "dipoles_RNOG_200m_2.00km",
	"gen2r_200m_3km" : "dipoles_RNOG_200m_3.00km",
	"gen2r_100m_2km" : "dipoles_RNOG_100m_2.00km",
	"gen2r_100m_3km" : "dipoles_RNOG_100m_3.00km",
	"gen2r_surf_1km" : "surface_4LPDA_1dipole_RNOG_1.00km",
	"gen2r_surf_15km" : "surface_4LPDA_1dipole_RNOG_1.50km",
	"gen2r_20m_1km" : "dipoles_RNOG_20m_1.00km"
}


det_files_labels = ["gen2r_100m_3km", "gen2r_200m_3km", "gen2r_surf_15km"]
det_files_labels = ["gen2r_surf_15km", "gen2r_surf_1km"]
config_file = "config_Alv2009_nonoise_100ns"
sim_file = "D02single_dipole_250MHz"

for det_file_label in det_files_labels:
	for flavor in flavors:
		det_file = det_files_dict[det_file_label]
		redo_file='redo_list_'+det_file_label+'_'+flavor+'.npz'

		the_logEs = []
		the_czmins = []
		the_czmaxs = []
		the_jobs = []

		for iE in range(len(logEs)):
			for iC in range(len(coszenbins)-1):
				czen1 = coszenbins[iC]
				czen2 = coszenbins[iC + 1]
				E = energies[iE]
				num_parts, num_events = hp.get_number_of_parts_and_events(flavor, logEs[iE], czen1)
				for ijob in range(num_parts):
					the_name = f'{step2dir}/{det_file}/{config_file}/{sim_file}/{flavor}/{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}/{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}.part{ijob:06}.hdf5'
					exists = os.path.exists(the_name)
					if not exists:
						the_logEs.append(logEs[iE])
						the_czmins.append(czen1)
						the_czmaxs.append(czen2)
						the_jobs.append(ijob)
						# instructions = ""
						# instructions += the_name
						# with open(redo_file, 'a') as f:
						# 	f.write(instructions)
						# print("{} Does not exist!".format(the_name))

		the_logEs = np.asarray(the_logEs)
		the_czmins = np.asarray(the_czmins)
		the_czmaxs = np.asarray(the_czmaxs)
		the_jobs = np.asarray(the_jobs)

		np.savez(redo_file, 
			energies=the_logEs, 
			czmins=the_czmins, 
			czmaxs=the_czmaxs,
			jobs=the_jobs)

