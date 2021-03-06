import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

base_dir = "/data/user/brianclark/Gen2/simulation_input/"

step0dir = os.path.join(base_dir, f"secondaries_500km2", "step0")
if(not os.path.exists(step0dir)):
	os.makedirs(step0dir)

step1dir = os.path.join(base_dir, f"secondaries_500km2", "step1")
if(not os.path.exists(step1dir)):
	os.makedirs(step1dir)

coszenbins = hp.get_coszenbins()
logEs = hp.get_logEs()
energies = 10 ** logEs * units.eV

phimin = 0.*units.deg
phimax = 360.*units.deg

dX = 6 * units.km
volume = {'fiducial_xmin': -10 * units.km - dX,
		'fiducial_xmax': 10 * units.km + dX,
		'fiducial_ymin': -12.5 * units.km - dX,
		'fiducial_ymax': 12.5 * units.km + dX,
		'fiducial_zmin': -2.7 * units.km,
		'fiducial_zmax': 0,
		'full_zmin': -3.3 * units.km,
		'full_zmax': 0
		}

distance_cut_polynomial = np.polynomial.polynomial.Polynomial([-1.56610502e+02, 2.54131322e+01, -1.34932379e+00, 2.39984185e-02])

def get_distance_cut(shower_energy):
	return max(100 * units.m, 10 ** distance_cut_polynomial(np.log10(shower_energy)))

flavors = ["e", "mu", "tau"]

flavor_ids = {'e': [12,-12],
			 'mu': [14,-14],
			'tau': [16,-16]}

for flavor in flavors:
	for iE in range(len(logEs)):


		max_dist = get_distance_cut(10 ** logEs[iE])
		print(f"maximum radius for E = {10**logEs[iE]:.2g} is {max_dist/units.m:.0f}m")

		# the ice sheet at SP is 2.7km deep, we add 200meters to be save for 200m deep dipole simulations
		volume['fiducial_zmin'] = -min(max_dist + 200*units.m, 2.7 * units.km)  
		
		for iC in range(len(coszenbins) - 1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			E = energies[iE]
			thetamax = np.arccos(czen1)
			thetamin = np.arccos(czen2)
			pattern = f"{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}"
			num_parts, num_events = hp.get_number_of_parts_and_events(flavor, logEs[iE], czen1)
			print(pattern)
			
			folder = os.path.join(step0dir, flavor, f"{pattern}")
			if(not os.path.exists(folder)):
				os.makedirs(folder)

			folder1 = os.path.join(step1dir, flavor, f"{pattern}")
			if(not os.path.exists(folder1)):
				os.makedirs(folder1)

			for ijob in range(num_parts):
				
				instruction = ""
				instruction += 'from NuRadioMC.EvtGen.generator import generate_eventlist_cylinder\n'
				instruction += 'from NuRadioReco.utilities import units\n\n'
				out_filename = "in_" + f"{pattern}" + f".part{ijob:06}" + ".hdf5"
				start_event_id = int(ijob * (num_events*5)) + 1
				instruction += f"generate_eventlist_cylinder('{out_filename}', {num_events}, {E}, {E}, {volume},\n"
				instruction += f"thetamin={thetamin}, thetamax={thetamax}, phimin={phimin},\n"
				instruction += f"phimax={phimax}, \n"
				instruction += f"start_event_id={start_event_id},\n"
				instruction += f"proposal=True, proposal_config='config_PROPOSAL.json', n_events_per_file=None,\n"
				instruction += f"flavor={flavor_ids[flavor]},\n"
				instruction += f"proposal_kwargs={{'low_nu': 1 * units.PeV, 'min_energy_loss_nu': 1 * units.PeV}})\n"
				instruction += "\n"
				python_filename = f'{pattern}_{ijob:06d}.py'
				
				if(not os.path.exists(os.path.join(step0dir, flavor, pattern))):
					os.makedirs(os.path.join(step0dir, flavor, pattern))

				if(not os.path.exists(os.path.join(step1dir, flavor, pattern))):
					os.makedirs(os.path.join(step1dir, flavor, pattern))
				
				with open(os.path.join(step0dir, flavor, pattern, python_filename), 'w') as f:
					f.write(instruction)
