import numpy as np
import os

import helper as hp

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs

flavors = ["e", "mu", "tau"]
flavors = ["mu"]

step3dir = "/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step3"

detsim_files_dict = {
	"pa_100m_2.00km" : "D05phased_array_deep",
	"pa_100m_3.00km" : "D05phased_array_deep",
	"pa_200m_2.00km" : "D05phased_array_deep",
	"pa_200m_3.00km" : "D05phased_array_deep",
	"surface_4LPDA_PA_15m_RNOG_300K_1.00km" : "D09surface_4LPDA_pa_15m_250MHz",
	"surface_4LPDA_PA_15m_RNOG_300K_1.50km" : "D09surface_4LPDA_pa_15m_250MHz"
}

det_files_dict = {
	"gen2r_100m_2km" : "pa_100m_2.00km",
	"gen2r_100m_3km" : "pa_100m_3.00km",
	"gen2r_200m_2km" : "pa_200m_2.00km",
	"gen2r_200m_3km" : "pa_200m_3.00km",
	"gen2r_surf_1km" : "surface_4LPDA_PA_15m_RNOG_300K_1.00km",
	"gen2r_surf_15km" : "surface_4LPDA_PA_15m_RNOG_300K_1.50km",
}


det_files_labels = ["gen2r_100m_2km", "gen2r_100m_3km", "gen2r_200m_2km", "gen2r_200m_3km", "gen2r_surf_1km", "gen2r_surf_15km"]
# det_files_labels = ["gen2r_surf_15km"]
config_file = "config_Alv2009_noise_100ns"

# loop flavors
for flavor in flavors:

	# loop energies
	for iE in range(len(logEs)):
		if logEs[iE]<=19.5:
			continue
		
		# loop zeniths
		for iC in range(len(coszenbins)-1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]

			# if czen1 < -0.2:
			# 	continue

			E = energies[iE]
			num_parts, num_events = hp.get_number_of_parts_and_events(flavor, logEs[iE], czen1)
			
			# check all parts
			num_problems = 0
			for ijob in range(num_parts):

				good_list = np.array([1, 1, 1, 1, 1, 1]) # assume they are all bad

				# now, we much check each detector
				for idet, det_file_label in enumerate(det_files_labels):

					det_file = det_files_dict[det_file_label]
					sim_file = detsim_files_dict[det_file]

					the_name = f'{step3dir}/{det_file}/{config_file}/{sim_file}/{flavor}/{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}/pass2_{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}.part{ijob:06}.hdf5.tar.gz'
					exists = os.path.exists(the_name)
					if not exists:
						# the_logEs.append(logEs[iE])
						# the_czmins.append(czen1)
						# the_czmaxs.append(czen2)
						# the_jobs.append(ijob)
						good_list[idet] = 0 # we have a problem
					if exists:
						size = os.path.getsize(the_name)
						if size<3500: # check if the file is too small (that is, a file transfer issue seems to have happened, and we need to rerun...)
							# print("File {} is too small (size {})".format(the_name, size))
							# the_logEs.append(logEs[iE])
							# the_czmins.append(czen1)
							# the_czmaxs.append(czen2)
							# the_jobs.append(ijob)
							good_list[idet]=0 # we have a problem

				need_to_move = False
				if np.sum(good_list)!=6:
					num_problems+=1
					need_to_move = True
					# print('{}, {:.2f}, {:.1f}-{:.1f}, {}: {}'.format(flavor, logEs[iE], czen1, czen2, ijob, good_list))

				if need_to_move:
					print('     Moving {}, {:.2f}, {:.1f}-{:.1f}, {}: {}'.format(flavor, logEs[iE], czen1, czen2, ijob, good_list))				

					for idet, det_file_label in enumerate(det_files_labels):

						det_file = det_files_dict[det_file_label]
						sim_file = detsim_files_dict[det_file]

						the_name = f'{step3dir}/{det_file}/{config_file}/{sim_file}/{flavor}/{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}/pass2_{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}.part{ijob:06}.hdf5.tar.gz'
						the_dest = f'{step3dir}/{det_file}/{config_file}/{sim_file}/hold/pass2_{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}.part{ijob:06}.hdf5.tar.gz'
						exists = os.path.exists(the_name)
						if exists:
							os.rename(the_name, the_dest) # move the file
							# print("move {} -> {}".format(the_name, the_dest))
			
			print('{}, {:.2f}, {:.1f}-{:.1f}: {}/{}'.format(flavor, logEs[iE], czen1, czen2, num_problems, num_parts))



