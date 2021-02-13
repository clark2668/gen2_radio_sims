import numpy as np
import matplotlib.pyplot as plt
from NuRadioReco.utilities import units
import pickle


n_deep = 143
n_shallow = (273)
deep_det = 'pa_200m_2.00km'
deep_trigger = 'PA_4channel_100Hz'
shallow_det = 'surface_4LPDA_PA_15m_RNOG_300K_1.00km'
shallow_trigger = 'LPDA_2of4_100Hz'
flavors = ['e', 'mu', 'tau']

data_independent = np.genfromtxt(f'tabulated_veff_aeff_pa_200m_2.00km_surface_1.00km.csv', delimiter=',', skip_header=1, names=['logE', 'dveff', 'daff', 'sveff', 'saeff'])
energies = np.power(10.,data_independent['logE'])
real_total = np.zeros(len(energies))
real_deep_only = np.zeros(len(energies))
real_shallow_only = np.zeros(len(energies))
real_dual = np.zeros(len(energies))

for iF, flavor in enumerate(flavors):
	filename = f'overlap_{deep_det}_{deep_trigger}_{shallow_det}_{shallow_trigger}_{flavor}.pkl'
	data = pickle.load(open(filename, 'br'))
	for i, key in enumerate(data.keys()): # assume all have the same number of energies
		real_total[i] += data[key]['total_veff']
		real_deep_only[i] += data[key]['deep_only_veff']
		real_shallow_only[i] += data[key]['shallow_only_veff']
		real_dual[i] += data[key]['dual_veff']

real_total/=3
real_deep_only/=3
real_shallow_only/=3
real_dual/=3

markers=['C0o-', 'C1^-', 'C2D-', 'C3s-']

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1,2,1)
ax1.plot(energies, real_total, markers[0], label='array')
ax1.plot(energies, real_deep_only, markers[1], label='deep only')
ax1.plot(energies, real_shallow_only, markers[2], label='shallow only')
ax1.plot(energies, real_dual, markers[3], label='deep+shallow')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel(r'Veff [km$^3$ sr]')
ax1.legend()
ax1.set_title('trigger level')

ax2 = fig.add_subplot(1,2,2)
ax2.plot(energies, real_total, markers[0], label='array')
# ax2.plot(energies, (data_independent['dveff']*n_deep)+(data_independent['sveff']*n_shallow))

plt.tight_layout()
fig.savefig('veff.png', dpi=300)







