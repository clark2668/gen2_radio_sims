import numpy as np
import matplotlib.pyplot as plt
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
import pickle


flavors = ['e', 'mu', 'tau']
# flavors = ['e']
energies = np.zeros(9)
veffs = np.zeros((3,9))


for iF, flavor in enumerate(flavors):
	filename = 'data/review_array_dict_{}.pkl'.format(flavor)
	data = pickle.load(open(filename, 'br'))
	for dat in data:
		energy = np.log10(dat['energy'])
		ebin = int((energy-16)/0.5)
		energies[ebin] = dat['energy']
		# print('{:e}'.format(dat['veff']['combined_array'][0]*4*np.pi))
		veff = dat['veff']['combined_array'][0] * units.m**3
		veff *= 0.917 * 4 * np.pi
		# aeff = veff / cross_sections.get_interaction_length(np.power(10., float(energy))*units.eV)
		# aeff *= (0.917 * 4 * np.pi)
		veffs[iF][ebin]+=(veff/units.km**3)

veffs/=(3*20)
markers = ['C0o--', 'C1d-.', 'C2^:']


fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1,2,1)
total = veffs[0]+veffs[1]+veffs[2]
ax1.plot(energies, total, 'k-', label='total')
ax1.plot(energies, veffs[0], markers[0], label='e')
ax1.plot(energies, veffs[1], markers[1], label='mu')
ax1.plot(energies, veffs[2], markers[2], label='tau')
# 	ax1.plot(energies, real_deep_only, markers[1], label='deep only')
# 	ax1.plot(energies, real_shallow_only, markers[2], label='shallow only')
# 	ax1.plot(energies, real_dual, markers[3], label='deep+shallow')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel(r'Veff [km$^3$ sr]')
ax1.set_ylim([1E-1, 1E4])
ax1.set_xlim([1E16, 1E20])
ax1.legend()
ax1.set_title('effective volume')

ax2 = fig.add_subplot(1,2,2)
ax2.plot(energies, veffs[0]/total, markers[0], label='e')
ax2.plot(energies, veffs[1]/total, markers[1], label='mu')
ax2.plot(energies, veffs[2]/total, markers[2], label='tau')
ax2.set_xscale('log')
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('fraction')
ax2.legend()
ax2.set_ylim([0,1])
ax2.set_title('fraction of triggers')
# ax2.plot(energies, (data_independent['dveff']*n_deep)+(data_independent['sveff']*n_shallow))

plt.tight_layout()
fig.savefig('aeff_by_flavor.png', dpi=300)

to_print = np.asarray(veffs[0]/total)

for e, fraction in zip(energies, to_print):
	print('E {}, fraction {:.2f}'.format(np.log10(e), fraction))


# data_i = np.genfromtxt(f'tabulated_veff_aeff_review_hybrid.csv', delimiter=',', skip_header=6, names=['logE', 'dveff', 'daff', 'sveff', 'saeff', 'overlap_frac', 'deep_only', 'shallow_only'])
# # data_i = np.genfromtxt(f'tabulated_veff_aeff_review_hybrid.csv', delimiter=',', skip_header=1, names=['logE', 'dveff', 'daff', 'sveff', 'saeff'])
# energies = np.power(10.,data_i['logE'])
# real_total = np.zeros(len(energies))
# real_deep_only = np.zeros(len(energies))
# real_shallow_only = np.zeros(len(energies))
# real_dual = np.zeros(len(energies))

# for iF, flavor in enumerate(flavors):
# 	filename = f'data/overlap_{deep_det}_{deep_trigger}_{shallow_det}_{shallow_trigger}_{flavor}.pkl'
# 	data = pickle.load(open(filename, 'br'))
# 	for i, key in enumerate(data.keys()): # assume all have the same number of energies
# 		real_total[i] += data[key]['total_veff']
# 		real_deep_only[i] += data[key]['deep_only_veff']
# 		real_shallow_only[i] += data[key]['shallow_only_veff']
# 		real_dual[i] += data[key]['dual_veff']

# real_total/=(3*units.km**3)
# real_deep_only/=(3*units.km**3)
# real_shallow_only/=(3*units.km**3)
# real_dual/=(3*units.km**3)

# # and needs a 4pi (dumb)
# real_total*=4*np.pi
# real_deep_only*=4*np.pi
# real_shallow_only*=4*np.pi
# real_dual*=4*np.pi

# markers=['ko-','C0o-', 'C1^-', 'C2D-', 'C3s-']

# plot_fractions=False
# if plot_fractions:

# 	fig = plt.figure(figsize=(10,5))
# 	ax1 = fig.add_subplot(1,2,1)
# 	ax1.plot(energies, real_total, markers[0], label='array')
# 	ax1.plot(energies, real_deep_only, markers[1], label='deep only')
# 	ax1.plot(energies, real_shallow_only, markers[2], label='shallow only')
# 	ax1.plot(energies, real_dual, markers[3], label='deep+shallow')
# 	ax1.set_xscale('log')
# 	ax1.set_yscale('log')
# 	ax1.set_xlabel('Energy [eV]')
# 	ax1.set_ylabel(r'Veff [km$^3$ sr]')
# 	ax1.set_ylim([1E-1, 5E4])
# 	ax1.legend()
# 	ax1.set_title('effective volume')

# 	ax2 = fig.add_subplot(1,2,2)
# 	ax2.plot(energies, real_deep_only/real_total, markers[1], label='deep only')
# 	ax2.plot(energies, real_shallow_only/real_total, markers[2], label='shallow only')
# 	ax2.plot(energies, real_dual/real_total, markers[3], label='deep+shallow')
# 	ax2.set_xscale('log')
# 	ax2.set_xlabel('Energy [eV]')
# 	ax2.set_ylabel('fraction')
# 	ax2.legend()
# 	ax2.set_ylim([0,1])
# 	ax2.set_title('fraction of triggers')
# 	# ax2.plot(energies, (data_independent['dveff']*n_deep)+(data_independent['sveff']*n_shallow))

# 	plt.tight_layout()
# 	fig.savefig('veff_and_fractions.png', dpi=300)

# plot_comparison = True
# if plot_comparison:

# 	fig = plt.figure(figsize=(10,5))
# 	ax1 = fig.add_subplot(1,2,1)
# 	ax1.plot(energies, real_total, markers[0], label='array "real"')
# 	# sum_to_plot = ((data_i['dveff']*n_deep + data_i['sveff']*n_shallow))
# 	sum_to_plot = ((data_i['dveff']*n_deep + data_i['sveff']*n_shallow)) * (1/(1+data_i['overlap_frac']))
# 	# sum_to_plot = (data_i['dveff']*n_deep*(data_i['overlap_frac']+data_i['deep_only'])) + (data_i['sveff']*n_shallow*(data_i['overlap_frac']+data_i['shallow_only']))
# 	# sum_to_plot = (data_i['dveff']*n_deep*data_i['deep_only']) + (data_i['sveff']*n_shallow*data_i['shallow_only']) + (data_i['dveff']*n_deep*(1-data_i['overlap_frac']))
# 	# sum_to_plot = ((data_i['dveff']*n_deep + data_i['sveff']*n_shallow)*(data_i['overlap_frac'])) + (data_i['dveff']*n_deep*data_i['deep_only']) + (data_i['sveff']*n_shallow*data_i['shallow_only'])
# 	ax1.plot(energies, sum_to_plot, markers[4]+'-', label='array estimate')
	
# 	# ax1.plot(energies, real_deep_only, markers[1], label='deep array')
# 	# ax1.plot(energies, data_i['dveff']*n_deep, markers[1]+'-', label='deep estimate')

# 	# ax1.plot(energies, real_deep_only, markers[1], label='deep only')
# 	# ax1.plot(energies, real_shallow_only, markers[2], label='shallow only')
# 	# ax1.plot(energies, real_dual, markers[3], label='deep+shallow')
# 	ax1.set_xscale('log')
# 	ax1.set_yscale('log')
# 	ax1.set_xlabel('Energy [eV]')
# 	ax1.set_ylabel(r'Veff [km$^3$ sr]')
# 	ax1.set_ylim([1E-1, 5E4])
# 	ax1.legend()
# 	ax1.set_title('effective volume')

# 	for thing in sum_to_plot/real_total-1.0:
# 		print('Thing {}'.format(thing))
# 	print(data_i['overlap_frac'])

# 	ax2 = fig.add_subplot(1,2,2)
# 	ax2.plot(energies, sum_to_plot / real_total, markers[4], label='estimate/real')
# 	ax2.set_xscale('log')
# 	ax2.set_xlabel('Energy [eV]')
# 	ax2.set_ylabel('unitless')
# 	ax2.legend()
# 	ax2.set_ylim([0,2])

# 	plt.tight_layout()
# 	fig.savefig('comparison.png', dpi=300)

# plot_independent_volume = False
# if plot_independent_volume:

# 	fig = plt.figure(figsize=(5,5))
# 	ax1 = fig.add_subplot(1,1,1)
# 	ax1.plot(energies, data_i['dveff'], markers[1], label='deep')
# 	ax1.plot(energies, data_i['sveff'], markers[2], label='shallow')
# 	ax1.set_title('single station veff')
# 	ax1.set_xscale('log')
# 	ax1.set_yscale('log')
# 	ax1.set_xlabel('Energy [eV]')
# 	ax1.set_ylabel(r'Veff [km$^3$ sr]')
# 	ax1.set_ylim([1E-3, 5E2])
# 	ax1.legend()

# 	plt.tight_layout()
# 	# fig.savefig('single_station_veffs_hybrid.png', dpi=300)
# 	fig.savefig('single_station_veffs_array.png', dpi=300)







