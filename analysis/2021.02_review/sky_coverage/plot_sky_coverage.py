import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from scipy import interpolate


n_deep = 144*1
n_shallow = (169+144)*1

deep_det = 'pa_200m_2.00km'
shallow_det = 'surface_1.00km'
filename=f'tabulated_aeff_vs_coszen_review_hybrid.csv'

data = np.genfromtxt(filename, delimiter=',', skip_header=6, names=['czmin', 'daeff', 'saeff', 'frac'])

plot_aeff_vs_zen = True
if plot_aeff_vs_zen:

	zen_for_interp = data['czmin']
	zen_for_interp+=0.05
	daeff_for_interp = data['daeff']
	saeff_for_interp = data['saeff']
	fractions = data['frac']

	zen_for_interp = np.flip(zen_for_interp)
	daeff_for_interp = np.flip(daeff_for_interp)
	saeff_for_interp = np.flip(saeff_for_interp)
	fractions = np.flip(fractions)

	# tck = interpolate.splrep(zen_for_interp, daeff_for_interp, k=2)
	interpolator_deep = scipy.interpolate.interp1d(zen_for_interp,daeff_for_interp,fill_value='extrapolate')
	interpolator_shallow = scipy.interpolate.interp1d(zen_for_interp,saeff_for_interp,fill_value='extrapolate')
	interpolator_fraction = scipy.interpolate.interp1d(zen_for_interp, fractions,fill_value='extrapolate')

	to_plot_x = np.linspace(-1,1,50)
	to_plot_y = (interpolator_deep(to_plot_x)*n_deep + interpolator_shallow(to_plot_x)*n_shallow)*(1/(1+interpolator_fraction(to_plot_x)))


	# plot of coverage vs zenith
	fig = plt.figure(figsize=(6,5))
	ax = fig.add_subplot(111)
	to_plot = (data['daeff']*n_deep + data['saeff']*n_shallow)*(1/(1+data['frac']))
	# ax.plot(data['czmin'], data['daeff']*n_deep, label='deep')
	# ax.plot(data['czmin'], data['saeff']*n_shallow, label='shallow')
	# ax.plot(-(data['czmin']+0.05), to_plot)
	ax.plot(-to_plot_x, to_plot_y)

	# 3dB point
	ax.plot([-1,1],[0.2,0.2], 'C7--')
	ax.annotate(r'"3dB Point"', xy=(-.95,0.22), xycoords='data', rotation=0, color='C7')

	ax.plot([-0.65,-0.65],[1e-7,1], 'C7--')
	ax.annotate(r'$\delta=-40^{\circ}$', xy=(-0.70,1e-2), xycoords='data', rotation=90, color='C7', size=12)

	ax.plot([0.005,0.005],[1e-7,1], 'C7--')
	ax.annotate(r'Horizon', xy=(-0.05,1e-2), xycoords='data', rotation=90, color='C7', size=12)
	
	# ax.set_xlabel(r'cos($\theta$)')
	ax.set_xlabel(r'sin($\delta$)',size=15)
	ax.set_ylabel(r'Aeff [$km^2$]',size=15)
	ax.set_yscale('log')
	plt.tight_layout()
	ax.set_ylim([5e-3,0.5])
	ax.set_xlim([-1,0.25])
	ax.tick_params(labelsize=12)
	ax.set_title('1 EeV',fontsize=15)
	plt.tight_layout()
	fig.savefig('aeff_vs_coszen.png',dpi=300)

doHealpyPlot = False
if doHealpyPlot:

	# pad a bit to get digitization to work right
	# zen_for_interp = np.append(data['czmin'], -1)
	# daeff_for_interp = np.insert(data['daeff'],0, data['daeff'][0])
	# saeff_for_interp = np.insert(data['saeff'],0, data['saeff'][0])
	# daeff_for_interp = np.append(data['daeff'], data['daeff'][-1])
	# saeff_for_interp = np.append(data['saeff'], data['saeff'][-1])

	zen_for_interp = data['czmin']
	zen_for_interp+=0.05
	daeff_for_interp = data['daeff']
	saeff_for_interp = data['saeff']
	fractions = data['frac']

	zen_for_interp = np.flip(zen_for_interp)
	daeff_for_interp = np.flip(daeff_for_interp)
	saeff_for_interp = np.flip(saeff_for_interp)
	fractions = np.flip(fractions)

	# tck = interpolate.splrep(zen_for_interp, daeff_for_interp, k=2)
	interpolator_deep = scipy.interpolate.interp1d(zen_for_interp,daeff_for_interp,fill_value='extrapolate')
	interpolator_shallow = scipy.interpolate.interp1d(zen_for_interp,saeff_for_interp,fill_value='extrapolate')
	interpolator_fraction = scipy.interpolate.interp1d(zen_for_interp, fractions,fill_value='extrapolate')

	# zen_bins_for_digi = data['czmin']
	# zen_bins_for_digi = np.insert(zen_bins_for_digi, 0, 1)
	# zen_bins_for_digi = np.append(zen_bins_for_digi,-1.)
	# zen_bin_to_aeff_dict = {A:B for A,B in zip(data['czmin'], data['daeff'])}

	import healpy as hlpy
	nside = 64
	npix = hlpy.nside2npix(nside)
	resolution = hlpy.nside2resol(nside, arcmin=True)/60
	scan = np.full(npix, hlpy.pixelfunc.UNSEEN)

	for ipix in range(npix):
		theta, phi = hlpy.pix2ang(nside, ipix) # where it's coming from
		cos_theta = -1 * np.cos(theta)
		# thebin = np.digitize(cos_theta, zen_bins_for_digi)
		# aeff_this  = data['daeff'][thebin-1]*n_deep + data['saeff'][thebin-1]*n_shallow
		# aeff_this = interpolate.splev(cos_theta, tck)
		aeff_this = (interpolator_deep(cos_theta)*n_deep + interpolator_shallow(cos_theta)*n_shallow)*(1/(1+interpolator_fraction(cos_theta)))
		# aeff_this = interpolator_fraction(cos_theta)
		if cos_theta > -2:
			# scan[ipix] = np.log10(aeff_this)
			# if(aeff_this<1E-4):
				# aeff_this=hlpy.pixelfunc.UNSEEN
			scan[ipix] = (aeff_this)

	# make the interpolator behave
	mask = scan < 0
	scan[mask]=0

	# mask = scan < np.max(scan)*0.5
	# scan[mask] = hlpy.pixelfunc.UNSEEN
	# maxval = np.max(scan)
	# scan/=maxval



	fig = plt.figure(figsize=(8,5))
	ax  = fig.add_subplot(111)
	plt.sca(ax)
	themap = hlpy.mollview(scan,
							title='1 EeV, {} deep, {} shallow'.format(n_deep,n_shallow),
							hold=True,
							# unit='\n'+r'$log_{10}(A_{eff}) [km^2]$',
							unit='\n'+r'$A_{eff} \,\,[km^2]$',
							# unit='\n'+r'Relative Effective Area',)
							min=0,
							max=0.40,
							cmap='Reds')
	hlpy.graticule()
	fig.savefig('sky_coverage_{}deep_{}shallow.png'.format(n_deep, n_shallow), dpi=300)



