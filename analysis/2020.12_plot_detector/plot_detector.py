import sys
import NuRadioReco.detector.detector as detector
from NuRadioReco.utilities import units
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

def plot_pa_passband():

	# passbands for the phasing
	passband_low = [96 * units.MHz, 100 * units.GHz]
	passband_high = [0 * units.MHz, 220 * units.MHz]
	order_low = 4
	order_high = 7
	ripple = 0.1
	filter_type = 'cheby1'

	ff = np.fft.rfftfreq(1024, 0.5 * units.ns)

	mask = ff > 0
	b_low, a_low = scipy.signal.cheby1(order_low, ripple, passband_low, 'bandpass', analog=True)
	w_low, h_low = scipy.signal.freqs(b_low, a_low, ff[mask])
	b_hi, a_hi = scipy.signal.cheby1(order_high, ripple, passband_high, 'bandpass', analog=True)
	w_hi, h_hi = scipy.signal.freqs(b_hi, a_hi, ff[mask])

	filt = h_low * h_hi
	gain = np.abs(filt)
	phase = np.angle(filt)
	unwrap = np.unwrap(phase)
	dF = ff[1]-ff[0]
	group_delay = np.diff(unwrap)/dF

	fig, axs_filt = plt.subplots(1, 3, figsize=(10,5))
	axs_filt[0].plot(ff[1:]/units.MHz, 20.*np.log10(gain), color='k')
	axs_filt[0].set_xlabel("Frequency [MHz]")
	axs_filt[0].set_ylabel("Gain [dB]")

	axs_filt[1].plot(ff[1:]/units.MHz, unwrap, color='k')
	axs_filt[1].set_xlabel("Frequency [MHz]")
	axs_filt[1].set_ylabel("Unwrapped Phase")

	axs_filt[2].plot(ff[2:]/units.MHz, group_delay, color='k')
	axs_filt[2].set_xlabel("Frequency [MHz]")
	axs_filt[2].set_ylabel("Group Delay [ns]")
	fig.tight_layout()

	fig.subplots_adjust(top=0.9)
	axs_filt[0].set_xlim(0, 300)
	axs_filt[0].set_ylim([-10,1])
	axs_filt[1].set_xlim(0,300)
	axs_filt[2].set_xlim(0,300)
	fig.suptitle("PA Trigger Antenna Filter")
	fig.savefig('pa_filter.png', dpi=300, edgecolor='none', bbox_inches='tight')

def plot_lpda_passband():

	# passbands for the phasing
	passband_low = [1 * units.MHz, 0.15*units.GHz]
	passband_high = [ 0.08*units.GHz, 800 * units.GHz]
	order_low = 10
	order_high = 5
	ripple = 0.1
	filter_type = 'cheby1'

	ff = np.fft.rfftfreq(1024, 0.5 * units.ns)

	mask = ff > 0
	b_low, a_low = scipy.signal.butter(order_low, passband_low, 'bandpass', analog=True)
	w_low, h_low = scipy.signal.freqs(b_low, a_low, ff[mask])
	b_hi, a_hi = scipy.signal.butter(order_high, passband_high, 'bandpass', analog=True)
	w_hi, h_hi = scipy.signal.freqs(b_hi, a_hi, ff[mask])

	filt = h_low * h_hi
	gain = np.abs(filt)
	phase = np.angle(filt)
	unwrap = np.unwrap(phase)
	dF = ff[1]-ff[0]
	group_delay = np.diff(unwrap)/dF

	fig, axs_filt = plt.subplots(1, 3, figsize=(10,5))
	axs_filt[0].plot(ff[1:]/units.MHz, 20.*np.log10(gain), color='k')
	axs_filt[0].set_xlabel("Frequency [MHz]")
	axs_filt[0].set_ylabel("Gain [dB]")

	axs_filt[1].plot(ff[1:]/units.MHz, unwrap, color='k')
	axs_filt[1].set_xlabel("Frequency [MHz]")
	axs_filt[1].set_ylabel("Unwrapped Phase [rad]")

	axs_filt[2].plot(ff[2:]/units.MHz, group_delay, color='k')
	axs_filt[2].set_xlabel("Frequency [MHz]")
	axs_filt[2].set_ylabel("Group Delay [ns]")
	fig.tight_layout()

	fig.subplots_adjust(top=0.9)
	axs_filt[0].set_xlim(0, 300)
	axs_filt[0].set_ylim([-10,1])
	axs_filt[1].set_xlim(0,300)
	axs_filt[2].set_xlim(0,300)
	axs_filt[2].set_ylim(-200,10)
	fig.suptitle("LPDA Trigger Antenna Filter")
	fig.savefig('lpda_filter.png', dpi=300, edgecolor='none', bbox_inches='tight')


def plot_deep_detectors():
	scale=1000
	det_files_deep = ['pa_100m_2.00km.json', 'pa_200m_3.00km.json']
	det_file_to_label_map = {
		'pa_100m_2.00km.json' : '2km spacing',
		'pa_100m_3.00km.json' : '3km spacing',
		'pa_200m_3.00km.json' : '3km spacing'
	}

	det_file_to_depth_map = {
		'pa_100m_2.00km.json' : '100m deep',
		'pa_100m_3.00km.json' : '100m deep',
		'pa_200m_3.00km.json' : '200m deep'
	}

	# top down
	fig_deep = plt.figure(figsize=(6,5))
	ax_deep = fig_deep.add_subplot(111)
	markers = ['o', 'x']

	fig_deep_side, axs_deep_side = plt.subplots(1,2, figsize=(10,5))

	for idet, det_file in enumerate(det_files_deep):

		det = detector.Detector(json_filename='det_files/'+det_file, antenna_by_depth=False, create_new=True)
		det.update(Time.now())

		station_ids = det.get_station_ids()

		# side view
		local_x = []
		z_8chan = []
		z_4chan = []
		n_channels = det.get_number_of_channels(1)
		for channel_id in range(n_channels):
			loc = det.get_relative_position(1, channel_id) + det.get_absolute_position(1)
			z_8chan.append(loc[2])
			if channel_id in range(2,6):
				z_4chan.append(loc[2])
			local_x.append(0)
		axs_deep_side[idet].plot(local_x, z_8chan, 'kd', label='8 ch PA')
		axs_deep_side[idet].plot(local_x[0:4], z_4chan, 'rx', markersize=12, linewidth=12, label='4 ch PA')
		axs_deep_side[idet].set_title(det_file_to_depth_map[det_file], size=15)

		# top down view
		x = []
		y = []

		station_ids = det.get_station_ids()
		for station_id in station_ids:
			loc = det.get_absolute_position(station_id)
			x.append(loc[0]/scale)
			y.append(loc[1]/scale)

		ax_deep.plot(x, y, markers[idet], label=det_file_to_label_map[det_file])

	# top down figure
	for ax in axs_deep_side.reshape(-1):
		ax.set_xlabel(r'X [m]', size=15)
		ax.set_ylabel(r'Depth [m]', size=15)
		ax.set_xlim([-2.5, 2.5])
		ax.set_aspect('equal')
		ax.tick_params(labelsize=15)
		ax.legend(loc='lower left')
	plt.tight_layout()
	fig_deep_side.savefig('deep_detectors_side.png', dpi=300, edgecolor='none', bbox_inches='tight')

	# side figure
	ax_deep.set_xlabel(r'Easting [km]',size=15)
	ax_deep.set_ylabel(r'Northing [km]',size=15)
	ax_deep.set_xlim([-15000/scale, 15000/scale])
	ax_deep.set_ylim([-15000/scale, 15000/scale])
	ax_deep.set_aspect('equal')
	ax_deep.tick_params(labelsize=15)
	ax_deep.legend()
	plt.tight_layout()
	fig_deep.savefig('deep_detectors.png', dpi=300, edgecolor='none', bbox_inches='tight')


def plot_shallow_detectors():
	scale=1000
	det_files_deep = ['surface_4LPDA_PA_15m_RNOG_1.00km.json', 'surface_4LPDA_PA_15m_RNOG_1.50km.json']
	det_file_to_label_map = {
		'surface_4LPDA_PA_15m_RNOG_1.00km.json' : '1 km spacing',
		'surface_4LPDA_PA_15m_RNOG_1.50km.json' : '1.5 km spacing',
	}

	# top down
	fig_deep = plt.figure(figsize=(6,5))
	ax_deep = fig_deep.add_subplot(111)
	markers = ['o', 'x']
	colors = ['C0', 'C3']

	fig_deep_side, axs_deep_side = plt.subplots(1,1, figsize=(5,5))
	fig_top_station, ax_top_station = plt.subplots(1,1, figsize=(5,5))

	for idet, det_file in enumerate(det_files_deep):

		det = detector.Detector(json_filename='det_files/'+det_file, antenna_by_depth=False, create_new=True)
		det.update(Time.now())

		station_ids = det.get_station_ids()

		if idet==0:
			# side view
			local_x_8chan = []
			local_x_4chan = []
			local_x_lpda = []
			z_lpda = []
			z_8chan = []
			z_4chan = []
			n_channels = det.get_number_of_channels(1)
			for channel_id in range(n_channels):
				loc = det.get_relative_position(1, channel_id)
				if channel_id < 4:
					local_x_lpda.append(loc[0])
					z_lpda.append(loc[2])
				else:
					z_8chan.append(loc[2])
					local_x_8chan.append(loc[0])
					if channel_id in range(6,10):
						z_4chan.append(loc[2])
						local_x_4chan.append(loc[0])
			axs_deep_side.plot(local_x_lpda, z_lpda, 'C0v', label='LPDAs')
			axs_deep_side.plot(local_x_8chan, z_8chan, 'kd', label='8 ch PA')
			axs_deep_side.plot(local_x_4chan, z_4chan, 'rx', markersize=12, linewidth=12, label='4 ch PA')

			# top down view of station
			local_x_lpda= []
			local_y_lpda = []
			local_x_dipoles = []
			local_y_dipoles = []
			n_channels = det.get_number_of_channels(1)
			for channel_id in range(n_channels):
				loc = det.get_relative_position(1, channel_id)
				if channel_id < 4:
					the_x = loc[0]
					the_y = loc[1]
					x_for_plotting = []
					y_for_plotting = []
					if abs(the_y) > 1:
						# top or bottom antenna
						x_for_plotting.append(the_x+0.5)
						x_for_plotting.append(the_x-0.5)
						y_for_plotting.append(the_y)
						y_for_plotting.append(the_y)
					else:
						# right or left antenna
						x_for_plotting.append(the_x)
						x_for_plotting.append(the_x)
						y_for_plotting.append(the_y+0.5)
						y_for_plotting.append(the_y-0.5)
					if channel_id==1:
						ax_top_station.plot(x_for_plotting, y_for_plotting, 'C0', 
							linewidth=4,
							label='LPDAs')
					else:
						ax_top_station.plot(x_for_plotting, y_for_plotting, 'C0',
							linewidth=4)
				else:
					local_x_dipoles.append(loc[0])
					local_y_dipoles.append(loc[1])
			ax_top_station.plot(local_x_dipoles, local_y_dipoles, 'ro', label='PA String')

		# top down view of array
		x = []
		y = []

		station_ids = det.get_station_ids()
		print("Num stations is {}".format(len(station_ids)))
		for station_id in station_ids:
			loc = det.get_absolute_position(station_id)
			x.append(loc[0]/scale)
			y.append(loc[1]/scale)

		ax_deep.plot(x, y, markers[idet],
			markersize=3,
			# color=colors[idet],
			label=det_file_to_label_map[det_file])

	# side figure of single station
	axs_deep_side.set_xlabel(r'X [m]', size=15)
	axs_deep_side.set_ylabel(r'Depth [m]', size=15)
	axs_deep_side.set_xlim([-3.5, 3.5])
	axs_deep_side.set_ylim([-25, 1])
	# axs_deep_side.set_aspect('equal')
	axs_deep_side.set_title("Side View")
	axs_deep_side.tick_params(labelsize=15)
	axs_deep_side.legend(loc='lower left')
	axs_deep_side.legend()
	plt.tight_layout()
	fig_deep_side.savefig('shallow_detectors_side.png', dpi=300, edgecolor='none', bbox_inches='tight')

	# top down figure of single station
	ax_top_station.set_xlabel(r'X [m]',size=15)
	ax_top_station.set_ylabel(r'Y [m]',size=15)
	ax_top_station.set_xlim([-3.5, 3.5])
	ax_top_station.set_aspect('equal')
	ax_top_station.tick_params(labelsize=15)
	ax_top_station.legend()
	ax_top_station.set_title("Top Down View")
	plt.tight_layout()
	fig_top_station.savefig('shallow_detectors_topdown_station.png', dpi=300, edgecolor='none', bbox_inches='tight')

	# top down figure of array	
	ax_deep.set_xlabel(r'Easting [km]',size=15)
	ax_deep.set_ylabel(r'Northing [km]',size=15)
	ax_deep.set_xlim([-15000/scale, 15000/scale])
	ax_deep.set_ylim([-15000/scale, 15000/scale])
	ax_deep.set_aspect('equal')
	ax_deep.tick_params(labelsize=15)
	ax_deep.legend()
	plt.tight_layout()
	fig_deep.savefig('shallow_detectors.png', dpi=300, edgecolor='none', bbox_inches='tight')



plot_shallow_detectors()
# plot_pa_passband()
# plot_lpda_passband()
