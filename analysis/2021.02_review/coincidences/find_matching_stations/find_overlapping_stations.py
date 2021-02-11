import NuRadioReco.detector.detector as detector
from astropy.time import Time

det_deep = detector.Detector(json_filename='pa_200m_2.00km.json', antenna_by_depth=False, create_new=True)
det_deep.update(Time.now())
deep_station_ids = det_deep.get_station_ids()

det_shallow = detector.Detector(json_filename='surface_4LPDA_PA_15m_RNOG_300K_1.00km.json', antenna_by_depth=False, create_new=False)

for d_id in deep_station_ids:
	loc_deep = det_deep.get_absolute_position(d_id)
	print("Station {}, Deep {}".format(d_id, loc_deep))

print(det_deep)
print(det_shallow)
print(det_deep)

# for s_id in shallow_station_ids:
# 	loc_shallow = det_shallow.get_absolute_position(s_id)
# 	print("Station {}, Shallow {}".format(s_id, loc_shallow))


# for deep_station in deep_station_ids:
# 	loc_deep = det_deep.get_absolute_position(deep_station)
# 	loc_shallow = det_shallow.get_absolute_position(deep_station)
# 	print("Station {}, Deep {}, Shallow {}".format(deep_station, loc_deep, loc_shallow))
