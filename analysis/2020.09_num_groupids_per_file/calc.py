import numpy as np
import h5py
import NuRadioMC.utilities.Veff
import helper as hp
import os
import glob
import matplotlib.pyplot as plt

# flavors=['e', 'mu', 'tau']
# flavors=['e']
flavors=['mu', 'tau']

def calc_n_events(fin):
	n_events = fin.attrs['n_events']
	n_groups = len(np.array(fin['event_group_ids']))
	n_groups_unique = len(np.unique(np.array(fin['event_group_ids'])))
	return n_events, n_groups, n_groups_unique

mydict = {}
for flavor in flavors:
	mydict[flavor] = []
	head_dir = f"/data/user/brianclark/Gen2/simulation_input/secondaries_500km2/step1/{flavor}/{flavor}_20.00eV_0.0_0.1"
	glob_filename = f"{head_dir}/*.hdf5"
	filenames = sorted(glob.glob(glob_filename))
	for fin in filenames:
		hdf5_in = h5py.File(fin, 'r')
		n_events, n_groups, n_groups_unique = calc_n_events(hdf5_in)
		print(f"{n_events}, {n_groups}, {n_groups_unique}")
		mydict[flavor].append(n_groups_unique)


fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
for flavor in flavors:
	mydict[flavor] = np.asarray(mydict[flavor])
	ax.hist(x=mydict[flavor], bins=np.arange(150), label=flavor, alpha=0.5)
ax.set_xlabel(r'Number of Unique Group IDs',size=15)
ax.set_ylabel(r'Number of Input Files',size=15)
ax.axvline(50, 0, 50, color='k', linestyle='--')
ax.set_title(r'cos($\theta$)=0.0-0.1, $E_{\nu}=10^{20}$eV',size=15)
ax.tick_params(labelsize=15)
ax.legend()
fig.savefig('num_unique_group_ids.png', edgecolor='none', bbox_inches='tight')

