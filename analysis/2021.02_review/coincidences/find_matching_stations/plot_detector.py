import sys
import NuRadioReco.detector.detector as detector
from NuRadioReco.utilities import units
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

scale = 1000.

# det_files = ['pa_200m_2.00km.json', 'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json', 'surface_4LPDA_PA_15m_RNOG_300K_1.50km.json']
# det_files = ['pa_200m_2.00km.json', 'surface_4LPDA_PA_15m_RNOG_300K_1.50km.json']
det_files = ['pa_200m_2.00km.json', 'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json']
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
markers = ['o', 'x', '+']
det_file_to_label_map = {
	'pa_200m_2.00km.json': 'Deep',
	'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json' : 'Surface 1km',
	'surface_4LPDA_PA_15m_RNOG_300K_1.50km.json' : 'Surface 1.5km',
}


for idet, det_file in enumerate(det_files):
	det = detector.Detector(json_filename=det_file, antenna_by_depth=False, create_new=True)
	det.update(Time.now())
	station_ids = det.get_station_ids()

	print('num stations {}'.format(len(station_ids)))

	x = []
	y = []

	station_ids = det.get_station_ids()
	for station_id in station_ids[0:10]:
		loc = det.get_absolute_position(station_id)
		print(loc)
		x.append(loc[0]/scale)
		y.append(loc[1]/scale)

	ax.plot(x, y, markers[idet], label=det_file_to_label_map[det_file])

# top down figure
ax.set_xlabel(r'X [m]', size=15)
ax.set_ylabel(r'Y [m]', size=15)
# ax.set_xlim([-2.5, 2.5])
ax.set_aspect('equal')
ax.tick_params(labelsize=15)
# ax.legend(loc='lower left')
plt.tight_layout()
fig.savefig('top_down.png', dpi=300, edgecolor='none', bbox_inches='tight')
