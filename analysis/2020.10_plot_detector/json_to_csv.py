import sys
import NuRadioReco.detector.detector as detector
from astropy.time import Time
import numpy as np

det = detector.Detector(json_filename=sys.argv[1], antenna_by_depth=False)
det.update(Time.now())

f = open(sys.argv[1]+'.csv', 'w')

station_ids = det.get_station_ids()
for station_id in station_ids:
	loc = det.get_absolute_position(station_id)
	f.write("{}, {}, {}\n".format(station_id, loc[0], loc[1]))
