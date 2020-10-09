import sys
import NuRadioReco.detector.detector as detector
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt


list_of_files = ['dipoles_RNOG_200m_2.00km.json', 'dipoles_RNOG_20m_1.00km.json']

dets = []
print(list_of_files)
for iF, file in enumerate(list_of_files):
	det = detector.Detector(json_filename=list_of_files[iF], antenna_by_depth=False, create_new=True)
	dets.append(det)
	print(det.get_station_ids())

print(dets)