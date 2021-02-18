import numpy as np
import matplotlib.pyplot as plt

data_gen2 = np.genfromtxt(f'gen2_optical_aeff.csv', delimiter=',', skip_header=1, names=['E', 'aeff'])
data_ic86_scale = np.genfromtxt(f'scaled_icecube_prl_veff.csv', delimiter=',', skip_header=1, names=['E', 'veff', 'aeff'])

energies_gen2 = np.power(10.,data_gen2['E'])
aeff_gen2 = data_gen2['aeff']

energies_scale = np.power(10.,data_ic86_scale['E'])
aeff_scale = data_ic86_scale['aeff']/4/np.pi # remove the sr

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1,2,1)
ax1.plot(energies_gen2, aeff_gen2, label='Gen2 from framework')
ax1.plot(energies_scale, aeff_scale, label='Scale IC86')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Energy [eV]')
ax1.set_ylabel(r'Aeff [m$^2$ sr]')
# ax1.set_ylim([1E-1, 5E4])
ax1.legend()

plt.tight_layout()
fig.savefig('gen2_vs_scaleic86.png', dpi=300)
