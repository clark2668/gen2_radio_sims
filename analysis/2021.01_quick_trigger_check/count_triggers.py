import h5py
import numpy as np
import NuRadioMC.utilities.Veff


path = "pass2_mu_20.00eV_0.0_0.1.part000000.hdf5"
f = h5py.File(path, 'r')

# something dan sent
# n_triggers = 0
# for i in range(len(np.array(f['event_group_ids']))):
# 	if(np.array(f['triggered'])[i]):
# 		n_triggers += 1

# print(n_triggers)


# something I wrote to count unique id's
# n_events = f.attrs['n_events']
# n_groups = len(np.array(f['event_group_ids']))
# n_groups_unique = len(np.unique(np.array(f['event_group_ids'])))


# print("n events {}".format(n_events))
# print("n groups {}".format(n_groups))
# print("n unique groups {}".format(n_groups_unique))

# something more I wrote to count weights
# n_events = f.attrs['n_events']
# uids, unique_mask = np.unique(np.array(f['event_group_ids']), return_index=True)
# weights = np.array(f['weights'])[unique_mask]
# n_triggered = np.sum(weights)

# print("num triggered is {}".format(n_triggered))

# and one more thing
# def calculate_trigger_stats_utility(fin):
# 	n_events = fin.attrs['n_events']
# 	simple_trigger_check = np.array(fin['triggered'])
# 	n_triggered=0
# 	if(simple_trigger_check.size!=0):
# 		# the 1.5 sigma dipole is trigger 1 [0=2.5sigma, 1=1.5 sigma]
# 		triggered = np.array(fin['multiple_triggers'][:, 2], dtype=np.bool)
# 		triggered = NuRadioMC.utilities.Veff.remove_duplicate_triggers(triggered, fin['event_group_ids'])
# 		weights = np.array(fin['weights'])
# 		n_triggered = np.sum(weights[triggered])

# 	return n_triggered, n_events

# triggered, n_events = calculate_trigger_stats_utility(f)
# print("N triggered {}, n events {}".format(triggered, n_events))
print(f['multiple_triggers'].keys())



