import sys
import NuRadioReco.detector.detector as detector
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt


list_of_files = ['dipoles_RNOG_200m_2.00km.json.csv', 'dipoles_RNOG_20m_1.00km.json.csv']
data_200 = np.genfromtxt(list_of_files[0], delimiter=',', skip_header=0, names=['id', 'x', 'y'])
data_20 = np.genfromtxt(list_of_files[1], delimiter=',', skip_header=0, names=['id', 'x', 'y'])

list_depths = ['200m', '20m']

dict_coords = {
	'200m' : data_200,
	'20m' : data_20
}


fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

markers = ['o', 'x']

for iF, depth in enumerate(list_depths):
	ax.plot(dict_coords[depth]['x'], dict_coords[depth]['y'], markers[iF], label=depth)

ax.set_xlabel(r'Easting',size=15)
ax.set_ylabel(r'Northing',size=15)
ax.tick_params(labelsize=15)
ax.legend()
fig.savefig('station_grid.png', edgecolor='none', bbox_inches='tight')
