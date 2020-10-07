import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import helper as hp

def get_struct(n_showers):
	sg = {}
	sg['shower_id'] = np.zeros(n_showers, dtype=np.int) * -1
	return sg

data_200 = np.genfromtxt('dipoles_RNOG_200m_2.00km.json.csv', delimiter=',', skip_header=0, names=['id', 'x', 'y'])

inputfilename = sys.argv[1]
fin, fin_stations, fin_attrs = hp.read_input_hdf5_file(inputfilename)

group_ids = fin['event_group_ids']
group_ids_unique = np.unique(np.array(group_ids))
num_events=0
for i_event_group_id, event_group_id in enumerate(group_ids_unique):
	if num_events>50:
		continue
	num_events+=1
	event_indices = np.atleast_1d(np.squeeze(np.argwhere(group_ids == event_group_id)))
	iE_mother = event_indices[0]
	x_int_mother = fin['xx'][iE_mother], fin['yy'][iE_mother], fin['zz'][iE_mother]
	energy_mother = fin['energies'][iE_mother]
	zenith_mother = fin['zeniths'][iE_mother]
	azimuth_mother = fin['azimuths'][iE_mother]
	shower_ids = np.array(fin['shower_ids'])
	x = []
	y = []
	z = []
	times = []
	energies = []
	for iSh, shower_index in enumerate(event_indices):
		shower_energy = fin['shower_energies'][shower_index]
		num_vhe=0
		if(shower_energy<1e16):
			continue
		shower_location = fin['xx'][shower_index], fin['yy'][shower_index], fin['zz'][shower_index]
		x.append(shower_location[0])
		y.append(shower_location[1])
		z.append(shower_location[2])
		times.append(fin['vertex_times'][shower_index]+1)
		energies.append(shower_energy)

	x = np.asarray(x)
	y = np.asarray(y)
	z = np.asarray(z)
	times = np.asarray(times)
	energies = np.asarray(energies)

	rescale=1e3
	my_map = plt.cm.viridis

	x/=rescale
	y/=rescale
	z/=rescale

	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111)
	ax.plot(data_200['x']/rescale, data_200['y']/rescale,'ko',alpha=0.3)
	sc = ax.scatter(x,y,c=times, norm=matplotlib.colors.LogNorm(), cmap=my_map)
	# ax.annotate("",xy=(x[-1],y[-1]),xytext=(x[0],y[0]), arrowprops=dict(arrowstyle="->"))
	ax.set_ylim([-2e4/rescale, 2e4/rescale])
	ax.set_xlim([-2e4/rescale, 2e4/rescale])
	cbar = plt.colorbar(sc)
	cbar.set_label(r'Times [ns]', size=15)
	ax.set_xlabel(r'Easting [km]',size=15)
	ax.set_ylabel(r'Northing [km]',size=15)
	ax.tick_params(labelsize=15)
	ax.set_aspect('equal')
	fig.savefig('event_times_top{}.png'.format(iE_mother), edgecolor='none', bbox_inches='tight')
	plt.close(fig)

	fig = plt.figure(figsize=(20, 5))
	ax = fig.add_subplot(111)
	sc = ax.scatter(x,z,c=times, norm=matplotlib.colors.LogNorm(), cmap=my_map)
	ax.set_ylim([-3e3/rescale, 0/rescale])
	ax.set_xlim([-2e4/rescale, 2e4/rescale])
	cbar = plt.colorbar(sc)
	cbar.set_label(r'Times [ns]', size=15)
	ax.set_xlabel(r'Easting [km]',size=15)
	ax.set_ylabel(r'Depth [km]',size=15)
	ax.tick_params(labelsize=15)
	# ax.set_aspect(3/40)
	fig.savefig('event_times_side{}.png'.format(iE_mother), edgecolor='none', bbox_inches='tight')
	plt.close(fig)

	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111)
	ax.plot(data_200['x']/rescale, data_200['y']/rescale,'ko',alpha=0.3)
	sc = ax.scatter(x,y,c=energies/1e9, norm=matplotlib.colors.LogNorm(), cmap=my_map)
	ax.set_ylim([-2e4/rescale, 2e4/rescale])
	ax.set_xlim([-2e4/rescale, 2e4/rescale])
	cbar = plt.colorbar(sc)
	cbar.set_label(r'Energy Deposited [GeV]', size=15)
	ax.set_xlabel(r'Easting [km]',size=15)
	ax.set_ylabel(r'Northing [km]',size=15)
	ax.tick_params(labelsize=15)
	ax.set_aspect('equal')
	fig.savefig('event_energies_{}.png'.format(iE_mother), edgecolor='none', bbox_inches='tight')
	plt.close(fig)
