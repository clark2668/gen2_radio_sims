import numpy as np
import os

from NuRadioReco.utilities import units

base_dir = "/data/user/brianclark/Gen2/simulation_input/"
working_dir = os.path.join(base_dir, f"secondaries_500km2", "step0")

if(not os.path.exists(working_dir)):
	os.makedirs(working_dir)

coszenbins = np.linspace(-1, 1, 21)
logEs = np.arange(15., 20.1, 0.5)
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

def get_number_of_events(logE):
	return 1e3

distance_cut_polynomial = np.polynomial.polynomial.Polynomial([-1.56610502e+02, 2.54131322e+01, -1.34932379e+00, 2.39984185e-02])

def get_distance_cut(shower_energy):
	return max(100 * units.m, 10 ** distance_cut_polynomial(np.log10(shower_energy)))

n_parts = 2

n_parts_per_file = np.ones(len(coszenbins)-1, dtype=np.int) * 1

flavors = ["e", "mu", "tau"]

flavor_ids = {'e': [12,-12],
			 'mu': [14,-14],
			'tau': [16,-16]}

for flavor in flavors:
	for iE in range(len(logEs)):
		if(logEs[iE]<20.0):
			continue
		# print (logEs[iE])
		nevt = get_number_of_events(logEs[iE])
		max_dist = get_distance_cut(10 ** logEs[iE])
		print(f"maximum radius for E = {10**logEs[iE]:.2g} is {max_dist/units.m:.0f}m")

		# the ice sheet at SP is 2.7km deep, we add 200meters to be save for 200m deep dipole simulations
		volume['fiducial_zmin'] = -min(max_dist + 200*units.m, 2.7 * units.km)  
		
		for iC in range(len(coszenbins) - 1):
			czen1 = coszenbins[iC]
			czen2 = coszenbins[iC + 1]
			if(czen2 > .3 or czen1 < -0.3):
				continue
			E = energies[iE]
			thetamax = np.arccos(czen1)
			thetamin = np.arccos(czen2)
			pattern = f"{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}"
			print(pattern)
			folder = os.path.join(working_dir, flavor, f"{pattern}")
			if(not os.path.exists(folder)):
				os.makedirs(folder)

			for ijob in range(n_parts//n_parts_per_file[iC]):
				
				instruction = ""
				instruction += 'from NuRadioMC.EvtGen.generator import generate_eventlist_cylinder\n'
				instruction += 'from NuRadioReco.utilities import units\n\n'
				for ipart in range(ijob * n_parts_per_file[iC], (ijob + 1) * n_parts_per_file[iC]):
					out_filename = f"{pattern}" + f".part{ipart:06}" + ".hdf5"
					start_event_id = int(ipart * nevt) + 1
					instruction += f"generate_eventlist_cylinder('{out_filename}', {nevt}, {E}, {E}, {volume},\n"
					instruction += f"thetamin={thetamin}, thetamax={thetamax}, phimin={phimin},\n"
					instruction += f"phimax={phimax}, \n"
					instruction += f"start_event_id={start_event_id},\n"
					instruction += f"proposal=True, proposal_config='SouthPole', n_events_per_file=None,\n"
					instruction += f"flavor={flavor_ids[flavor]},\n"
					instruction += f"proposal_kwargs={{'low_nu': 1 * units.PeV, 'min_energy_loss_nu': 1 * units.PeV}})\n"
					instruction += "\n"
				
				python_filename = f'{pattern}_{ijob:06d}.py'
				
				if(not os.path.exists(os.path.join(working_dir, flavor, pattern))):
					os.makedirs(os.path.join(working_dir, flavor, pattern))
				
				with open(os.path.join(working_dir, flavor, pattern, python_filename), 'w') as f:
					f.write(instruction)
