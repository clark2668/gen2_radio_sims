import pickle


'''
so the pickle files are organized with an entry for each energy bin and each zenith bin
for every energy and zenith bin, I need to specify:
	- 'energy' (in eV)
	- 'energy_min' (in eV)
	- 'enerny_max' (in eV)
	- 'domega' (in radians), should just be 0.6283185307179577
	- 'thetamin (in radians)
	- 'thetamax' (inr adians)
	- 'depostied' = False
	- 'veff' dictionary, one key for every trigger; for each dictionary, need veff, veff error, summed weights, veff lo, and veff high
'''



filename = '/data/sim/Gen2/radio/2020/simulation_output/secondaries_500km2/step5/DETECTOR_pa_100m_2.00km_____CONFIG_config_Alv2009_noise_100ns_____SIM_D05phased_array_deep_____FLAVOR_mu.pkl'
data = pickle.load(open(filename, 'br'))
print('length of data {}'.format(len(data)))
for thing in data:
	print(thing)
	print('------')
# for i, key in enumerate(data.keys()):
# 	print('i {} is {}'.format(k, key))


