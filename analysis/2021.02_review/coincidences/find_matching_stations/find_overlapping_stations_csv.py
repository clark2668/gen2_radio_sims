import numpy as np

detectors = ['pa_200m_2.00km.json.csv', 'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json.csv']

deep_data = np.genfromtxt(detectors[0], delimiter=',', skip_header=0, names=['id', 'x', 'y'])
shallow_data = np.genfromtxt(detectors[1], delimiter=',', skip_header=0, names=['id', 'x', 'y'])

# load the deep data
deep_dict = {}
for i in range(len(deep_data)):
	deep_dict[int(deep_data['id'][i])] = [ deep_data['x'][i], deep_data['y'][i] ]

# load the shallow data
shallow_dict = {}
for i in range(len(shallow_data)):
	shallow_dict[int(shallow_data['id'][i])] = [ shallow_data['x'][i], shallow_data['y'][i] ]

shallow_match = []

for d_id in deep_dict:
	d_loc = deep_dict[d_id]
	for s_id in shallow_dict:
		s_loc = shallow_dict[s_id]
		if np.sqrt((d_loc[0]-s_loc[0])**2 + (d_loc[1]-s_loc[1])**2) < 0.01:
			print("Match! Deep {} ({}), Shallow {} ({})".format(d_id, d_loc, s_id, s_loc))
			shallow_match.append(s_id)

# write this to a file
f = open('deep_shallow_match.csv', 'w')
for d_id in deep_dict:
	print("Deep {}, Shallow {}".format(d_id, shallow_match[d_id-1]))
	f.write('{}, {} \n'.format(d_id, shallow_match[d_id-1]))
