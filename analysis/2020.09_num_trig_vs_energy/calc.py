import numpy as np
import h5py
import NuRadioMC.utilities.Veff
import helper as hp
import os
import glob
import matplotlib.pyplot as plt


def calculate_trigger_stats_basic(fin):
	n_events = fin.attrs['n_events']
	uids, unique_mask = np.unique(np.array(fin['event_group_ids']), return_index=True)
	weights = np.array(fin['weights'])[unique_mask]
	n_triggered = np.sum(weights)

	return n_triggered, n_events


def calculate_trigger_stats_utility(fin):
	n_events = fin.attrs['n_events']
	simple_trigger_check = np.array(fin['triggered'])
	n_triggered=0
	if(simple_trigger_check.size!=0):
		# the 1.5 sigma dipole is trigger 1 [0=2.5sigma, 1=1.5 sigma]
		triggered = np.array(fin['multiple_triggers'][:, 1], dtype=np.bool)
		triggered = NuRadioMC.utilities.Veff.remove_duplicate_triggers(triggered, fin['event_group_ids'])
		weights = np.array(fin['weights'])
		n_triggered = np.sum(weights[triggered])

	return n_triggered, n_events

head_dir = "/Users/brianclark/Documents/work/Gen2/hdf5_files"

logEs = hp.get_logEs()
# energies = 10 ** logEs

tot_n_triggered = []
tot_n_events = []
errors = []

for logE in logEs:
	glob_filename = f"{head_dir}/e_{logE:.2f}eV*.hdf5"
	filenames = sorted(glob.glob(glob_filename))
	this_E_n_triggered =0
	this_E_n_events = 0
	for fin in filenames:
		hdf5_in = h5py.File(fin, 'r')
		# if('trigger_names' in hdf5_in.attrs):
		# 	print(hdf5_in.attrs['trigger_names'])
		this_f_n_triggered, this_f_n_events = calculate_trigger_stats_utility(hdf5_in)
		this_E_n_triggered += this_f_n_triggered
		this_E_n_events += this_f_n_events

	tot_n_triggered.append(this_E_n_triggered)
	tot_n_events.append(this_E_n_events)
	fraction = this_E_n_triggered/this_E_n_events
	error = fraction / this_E_n_triggered ** 0.5
	errors.append(error)

tot_n_triggered = np.asarray(tot_n_triggered)
tot_n_events = np.asarray(tot_n_events)
passing_fraction = tot_n_triggered/tot_n_events
errors = np.asarray(errors)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.errorbar(x=logEs, y=passing_fraction*100, yerr=errors*100, fmt='ko')
# ax.plot(logEs, passing_fraction*100, 'ko')
ax.set_xlabel(r'log$_{10}(E_{\nu}$)',size=15)
ax.set_ylabel(r'Fraction Passing Trigger',size=15)
ax.set_title(r'$\nu_{e}$, 100m dipole, 1.5$\sigma$ trigger, all-sky average',size=15)
ax.tick_params(labelsize=15)
ax.set_yscale('log')

fig.savefig('passing_fraction.png', edgecolor='none', bbox_inches='tight')

