import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from scipy import interpolate

data_200m = np.load('data/deep_only_200m_skycoverage.npz')
data_100m = np.load('data/deep_only_100m_skycoverage.npz')
data_shal = np.load('data/shallow_only_skycoverage.npz')
energies = np.log10(data_200m['energies'])
dets = ['200m', '100m', 'Surface']

def workout_3dB(interp):
	xvals = np.linspace(-1,1,100)
	yvals = interp(xvals)
	yvals /= np.max(yvals)

	points = []

	for i, yval in enumerate(yvals):
		if abs(yval-0.5)<0.1:
			points.append(xvals[i])

	return points

plot_aeff_vs_zen = True
if plot_aeff_vs_zen:

	zen_for_interp = data_200m['zen_bins']
	zen_for_interp+=0.05
	d_200_aeff = data_200m['aeff_vzen']*1e6
	d_100_aeff = data_100m['aeff_vzen']*1e6
	s_aeff = data_shal['aeff_vzen']*1e6

	dets_dict = {
		'200m':d_200_aeff,
		'100m':d_100_aeff,
		'Surface':s_aeff,
	}

	for i, e in enumerate(energies):
		if e!=17:
			continue

		interpolator_200 = scipy.interpolate.interp1d(zen_for_interp,d_200_aeff[i],fill_value='extrapolate')
		interpolator_100 = scipy.interpolate.interp1d(zen_for_interp,d_100_aeff[i],fill_value='extrapolate')
		interpolator_shal = scipy.interpolate.interp1d(zen_for_interp, s_aeff[i],fill_value='extrapolate')

		interp_dict = {
			'200m':interpolator_200,
			'100m':interpolator_100,
			'Surface':interpolator_shal,
		}

		# for det in dets:
		det = '100m'
		for det in dets:
		# if 1==1:
			
			# SUPER hacky way to find the 3dB points
			points = workout_3dB(interp_dict[det])
			minpoint = np.min(points)
			maxpoint = np.max(points)
			points = -np.array([minpoint, maxpoint])

			fig = plt.figure(figsize=(6,5))
			ax = fig.add_subplot(111)
			
			to_plot = dets_dict[det][i] # pick the detector and this energy bin
			to_plot_x = np.linspace(-1,1,50)
			to_plot_y = interp_dict[det](to_plot_x)
			# ax.plot(-zen_for_interp, to_plot, label=det+'raw')
			ax.plot(-to_plot_x, to_plot_y, label=det+', log10(E)={}'.format(e))
			start = 1e-1
			end = 1e3
			end = 20e4
			end = 20
			end = 40
			ax.plot([points[0], points[0]],[start,end], 'C7--', linewidth=2, label=r'3dB $\delta$={:.2f}$^\circ$'.format(np.rad2deg(np.arcsin(points[0]))))
			ax.plot([points[1], points[1]],[start,end], 'C7-.', linewidth=2, label=r'3dB $\delta$={:.2f}$^\circ$'.format(np.rad2deg(np.arcsin(points[1]))))

			sky_cov_area = (180./np.pi)*(points[0]-points[1]) *360

			ax.legend()
			ax.set_xlabel(r'sin($\delta$)',size=20)
			ax.set_ylabel(r'Aeff [$m^2$]',size=20)
			ax.set_title("Sky coverage {:.2f} sq deg ({:.0f}% of whole sky) ".format(sky_cov_area, 100.*sky_cov_area/41252.96125))
			# ax.set_ylim(0,1800)
			# ax.set_ylim(0,40e3)
			ax.set_ylim(0,80) #1E17
			ax.tick_params(labelsize=15)
			plt.tight_layout()
			fig.savefig('aeff_vs_coszen_det_{}_e_{}.png'.format(det,e),dpi=300)

	# # plot of coverage vs zenith
	# 
	# 
	# to_plot = (data['daeff']*n_deep + data['saeff']*n_shallow)*(1/(1+data['frac']))
	# # ax.plot(data['czmin'], data['daeff']*n_deep, label='deep')
	# # ax.plot(data['czmin'], data['saeff']*n_shallow, label='shallow')
	# # ax.plot(-(data['czmin']+0.05), to_plot)
	# ax.plot(-to_plot_x, to_plot_y, linewidth=4)
	# # 3dB point
	# ax.plot([-1,1],[0.17,0.17], 'C7--', linewidth=2)
	# ax.annotate(r'"3dB Point"', xy=(-.99,0.20), xycoords='data', 
	# 	rotation=0, color='C7', fontsize=15)

	# ax.plot([-0.67,-0.67],[1e-7,1], 'C7--', linewidth=2)
	# ax.annotate(r'$\delta=-42^{\circ}$', xy=(-0.72,1e-2), xycoords='data', 
	# 	rotation=90, color='C7', size=15)

	# ax.plot([0.025,0.025],[1e-7,1], 'C7--', linewidth=2)
	# ax.annotate(r'$\delta=2^{\circ}$', xy=(-0.03,1e-2), xycoords='data', 
	# 	rotation=90, color='C7', size=15)
	
	# # ax.set_xlabel(r'cos($\theta$)')
	# ax.set_xlabel(r'sin($\delta$)',size=20)
	# ax.set_ylabel(r'Aeff [$km^2$]',size=20)
	# ax.set_yscale('log')
	# plt.tight_layout()
	# ax.set_ylim([5e-3,0.5])
	# ax.set_xlim([-1,0.25])
	# ax.tick_params(labelsize=15)
	# ax.set_title('1 EeV',fontsize=20)
	# plt.tight_layout()
	# fig.savefig('aeff_vs_coszen.png',dpi=300)

	# zen_for_interp = np.flip(zen_for_interp)
	# daeff_for_interp = np.flip(daeff_for_interp)
	# saeff_for_interp = np.flip(saeff_for_interp)
	# fractions = np.flip(fractions)

	# # tck = interpolate.splrep(zen_for_interp, daeff_for_interp, k=2)
	# interpolator_deep = scipy.interpolate.interp1d(zen_for_interp,daeff_for_interp,fill_value='extrapolate')
	# interpolator_shallow = scipy.interpolate.interp1d(zen_for_interp,saeff_for_interp,fill_value='extrapolate')
	# interpolator_fraction = scipy.interpolate.interp1d(zen_for_interp, fractions,fill_value='extrapolate')

	# to_plot_x = np.linspace(-1,1,50)
	# to_plot_y = (interpolator_deep(to_plot_x)*n_deep + interpolator_shallow(to_plot_x)*n_shallow)*(1/(1+interpolator_fraction(to_plot_x)))



