import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from scipy import interpolate


n_deep = 0 #144
n_shallow = (169+144)
uptime = 1.
which_e_bin = 6

deep_det = 'pa_200m_2.00km'
shallow_det = 'surface_1.00km'
filename=f'tabulated_aeff_vs_zen_{deep_det}_{shallow_det}_Ebin_{which_e_bin}.csv'

data = np.genfromtxt(filename, delimiter=',', skip_header=1, names=['czmin', 'daeff', 'saeff'])

# plot of coverage vs zenith
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.plot(data['czmin'], data['daeff']*n_deep*2, label='deep')
ax.plot(data['czmin'], data['saeff']*n_shallow*2, label='shallow')
ax.set_xlabel('coz(zen)')
ax.set_ylabel(r'Aeff $\times 2 \pi$ [$km^2$]')
ax.set_yscale('log')
ax.set_ylim([1e-3,10])
ax.legend()
ax.set_title('Trigger Level')
plt.tight_layout()
fig.savefig('aeff_vs_coszen.png')


# zen_for_interp = np.append(data['czmin'], -1)
# daeff_for_interp = np.append(data['daeff'], data['daeff'][-1])
# saeff_for_interp = np.append(data['saeff'], data['saeff'][-1])

zen_for_interp = data['czmin']
zen_for_interp-=0.05
daeff_for_interp = data['daeff']
saeff_for_interp = data['saeff']

zen_for_interp = np.flip(zen_for_interp)
daeff_for_interp = np.flip(daeff_for_interp)
saeff_for_interp = np.flip(saeff_for_interp)

# tck = interpolate.splrep(zen_for_interp, daeff_for_interp, k=2)
interpolator_deep = scipy.interpolate.interp1d(zen_for_interp,daeff_for_interp,fill_value='extrapolate')
interpolator_shallow = scipy.interpolate.interp1d(zen_for_interp,saeff_for_interp,fill_value='extrapolate')

zen_bins_for_digi = data['czmin']
zen_bins_for_digi = np.append(zen_bins_for_digi,-1.)
# zen_bin_to_aeff_dict = {A:B for A,B in zip(data['czmin'], data['daeff'])}

doHealpyPlot = True
if doHealpyPlot:

	import healpy as hlpy
	nside = 64
	npix = hlpy.nside2npix(nside)
	resolution = hlpy.nside2resol(nside, arcmin=True)/60
	scan = np.full(npix, hlpy.pixelfunc.UNSEEN)

	for ipix in range(npix):
		theta, phi = hlpy.pix2ang(nside, ipix) # where it's coming from
		cos_theta = -1 * np.cos(theta)
		thebin = np.digitize(cos_theta, zen_bins_for_digi)
		# aeff_this  = data['daeff'][thebin-1]*n_deep + data['saeff'][thebin-1]*n_shallow
		# aeff_this = interpolate.splev(cos_theta, tck)
		aeff_this = interpolator_deep(cos_theta)*n_deep + interpolator_shallow(cos_theta)*n_shallow
		if cos_theta > -2:
			# scan[ipix] = np.log10(aeff_this)
			# if(aeff_this<1E-4):
				# aeff_this=hlpy.pixelfunc.UNSEEN
			scan[ipix] = (aeff_this)

	# make the interpolator behave
	mask = scan < 0
	scan[mask]=0

	mask = scan < np.max(scan)*0.5
	scan[mask] = hlpy.pixelfunc.UNSEEN
	# maxval = np.max(scan)
	# scan/=maxval



	fig = plt.figure(figsize=(8,5))
	ax  = fig.add_subplot(111)
	plt.sca(ax)
	themap = hlpy.mollview(scan,
							title='1 EeV, {} deep, {} shallow',
							hold=True,
							# unit='\n'+r'$log_{10}(A_{eff}) [km^2]$',
							unit='\n'+r'$A_{eff} \,\,[km^2]$',
							# unit='\n'+r'Relative Effective Area',)
							cmap='Reds')
	hlpy.graticule()
	fig.savefig('sky_coverage_{}deep_{}shallow.png'.format(n_deep, n_shallow))



