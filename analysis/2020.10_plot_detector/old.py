import sys
import NuRadioReco.detector.detector as detector
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt


list_of_files = ['dipoles_RNOG_200m_2.00km.json', 'dipoles_RNOG_20m_1.00km.json']

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

markers = ['o', 'x']

dets = []
print(list_of_files)
for iF, file in enumerate(list_of_files):
	det = detector.Detector(json_filename=list_of_files[iF], antenna_by_depth=False)
	dets.append(det)
	# dets.append(file)

print(dets)

# for iF, file in enumerate(list_of_files):
# 	# det_filename = sys.argv[1]
# 	print(file)
# 	det = detector.Detector(json_filename=file, antenna_by_depth=False)
# 	det.update(Time.now())

# 	station_ids = det.get_station_ids()
# 	print(station_ids)

# 	xs = []
# 	ys = []

# 	for station_id in station_ids:
# 		loc = det.get_absolute_position(station_id)
# 		xs.append(loc[0])
# 		ys.append(loc[1])

# 	xs = np.asarray(xs)
# 	ys = np.asarray(ys)
# 	ax.plot(xs, ys, markers[iF])

# ax.set_xlabel(r'Easting',size=15)
# ax.set_ylabel(r'Northing',size=15)
# ax.set_title(r'Depth ',size=15)
# ax.tick_params(labelsize=15)
# fig.savefig('station_grid.png', edgecolor='none', bbox_inches='tight')
