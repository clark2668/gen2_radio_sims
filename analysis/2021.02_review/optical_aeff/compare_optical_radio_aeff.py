import matplotlib.pyplot as plt
import numpy as np
from gen2_analysis import factory, plotting

factory.set_kwargs(psi_bins={k: [0, np.pi] for k in ('tracks', 'cascades', 'radio')})
radio_aeff = factory.get('Gen2-Radio')['radio_events'][0]
gen2_aeff_cascades = factory.get('Gen2-InIce')['cascades'][0]
gen2_aeff_st = factory.get('Gen2-InIce')['shadowed_tracks'][0]
gen2_aeff_ut = factory.get('Gen2-InIce')['unshadowed_tracks'][0]

cos_theta = radio_aeff.bin_edges[radio_aeff.dimensions.index('true_zenith_band')-1]
flavors = ['${}$' .format([r'\nu', r'\overline{\nu}'][i % 2] + '_{' + ['e', r'\mu', r'\tau'][i/2] +'}') for i in range(6)]

# slice through things, because the cascades and tracks don't have the same ranges
energies_joint = gen2_aeff_cascades.bin_edges[0][1:][:-10]
# print('Cascade energies {}'.format(gen2_aeff_cascades.bin_edges[0][1:][:-10]))
# print('Track energies {}'.format(gen2_aeff_st.bin_edges[0][1:][30:]))

cascades_e = gen2_aeff_cascades.values[0,...].mean(axis=1).sum(axis=(1,2))[:-10]
cascade_mu = gen2_aeff_cascades.values[2,...].mean(axis=1).sum(axis=(1,2))[:-10]
cascade_tau = gen2_aeff_cascades.values[4,...].mean(axis=1).sum(axis=(1,2))[:-10]
cascade_average = (cascades_e + cascade_mu + cascade_tau)/3
tracks_unshadowed = gen2_aeff_ut.values[2,...].mean(axis=1).sum(axis=(1,2))[30:]
tracks_shadowed = gen2_aeff_st.values[2,...].mean(axis=1).sum(axis=(1,2))[30:]
tracks_sum = tracks_unshadowed + tracks_shadowed

# 4/6 of the neutrinos are cascades (CC nue, NC nue, NC numu, NC nutau), and 2/6 are tracks (CC numu, CC nutau)
average_aeff = (cascade_average*4/6) + (tracks_sum*2/6)

output_csv = 'log10(energy) [eV], effective area [m^2]\n'
for i, e in enumerate(energies_joint):
	output_csv += '{:.1f}, {:e}\n'.format(np.log10(energies_joint[i]*1E9), average_aeff[i]*1E-6) # convert GeV to eV, and m^2 to km^2
with open('gen2_optical_aeff.csv', 'w') as fout:
	fout.write(output_csv)

fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
for i in range(0,6,2):
	# first, the radio aeff
	line = ax.loglog(radio_aeff.bin_edges[0][1:], radio_aeff.values[i,...].mean(axis=1).sum(axis=(1,2)), label='Radio, {}'.format(flavors[i]))[0]
	# then, the Gen2-Optical cascades, which is defined for all flavors
	# line = ax.loglog(gen2_aeff_cascades.bin_edges[0][1:], gen2_aeff_cascades.values[i,...].mean(axis=1).sum(axis=(1,2)), color=line.get_color(), ls='-.', label='Gen2-Optical Cascades, {}'.format(flavors[i]))[0]


# the tracks only seem to apply to nu-mu (i=2)
# shadowed tracks are those that come with with a IceTop veto; unshadowed tracks have no veto
# line = ax.loglog(gen2_aeff_ut.bin_edges[0][1:], gen2_aeff_ut.values[2,...].mean(axis=1).sum(axis=(1,2)), color='C1', ls='--', label='Gen2-Optical UnShadowed Tracks, {}'.format(flavors[2]))[0]
# line = ax.loglog(gen2_aeff_st.bin_edges[0][1:], gen2_aeff_st.values[2,...].mean(axis=1).sum(axis=(1,2)), color='C1', ls=':', label='Gen2-Optical Shadowed Tracks, {}'.format(flavors[2]))[0]
line = ax.loglog(energies_joint, average_aeff, color='C4', ls='-', label='Gen2-Optical all flavor average')

ax.set_ylabel(r'$\nu$ effective area (m$^2$)')
ax.set_xlabel(r'$\nu$ energy (GeV)')
ax.set_xlim(1e4, 5e10)
ax.set_ylim(1e-1, 5e6)

ax.legend()
plt.savefig('compare_aeff.png',dpi=300)

