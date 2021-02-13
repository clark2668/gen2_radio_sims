import numpy as np
import matplotlib.pyplot as plt

scale = 1000.

det_files = ['pa_200m_2.00km.json.csv', 'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json.csv']

markers = ['o', 'x', '+']
det_file_to_label_map = {
	'pa_200m_2.00km.json': 'Deep',
	'surface_4LPDA_PA_15m_RNOG_300K_1.00km.json' : 'Surface 1km',
	'surface_4LPDA_PA_15m_RNOG_300K_1.50km.json' : 'Surface 1.5km',
}

# we need to nuke 2-26:
to_remove = []
start = 2
while start <= 26:
	to_remove.append(int(start))
	start+=2
start = 54
while start <= 78:
	to_remove.append(int(start))
	start+=2
start = 106
while start <= 130:
	to_remove.append(int(start))
	start+=2
start = 158
while start <= 182:
	to_remove.append(int(start))
	start+=2
start = 210
while start <= 234:
	to_remove.append(int(start))
	start+=2
start = 262
while start <= 286:
	to_remove.append(int(start))
	start+=2
start = 314
while start <= 338:
	to_remove.append(int(start))
	start+=2
start = 366
while start <= 390:
	to_remove.append(int(start))
	start+=2
start = 418
while start <= 442:
	to_remove.append(int(start))
	start+=2
start = 470
while start <= 494:
	to_remove.append(int(start))
	start+=2
start = 522
while start <= 546:
	to_remove.append(int(start))
	start+=2


start = 27
while start <= 51:
	to_remove.append(int(start))
	start+=2
start = 79
while start <= 103:
	to_remove.append(int(start))
	start+=2
start = 131
while start <= 155:
	to_remove.append(int(start))
	start+=2
start = 183
while start <= 207:
	to_remove.append(int(start))
	start+=2
start = 235
while start <= 259:
	to_remove.append(int(start))
	start+=2
start = 287
while start <= 311:
	to_remove.append(int(start))
	start+=2
start = 339
while start <= 363:
	to_remove.append(int(start))
	start+=2
start = 391
while start <= 415:
	to_remove.append(int(start))
	start+=2
start = 443
while start <= 467:
	to_remove.append(int(start))
	start+=2
start = 495
while start <= 519:
	to_remove.append(int(start))
	start+=2

deep_data = np.genfromtxt(det_files[0], delimiter=',', skip_header=0, names=['id', 'x', 'y'])
shallow_data = np.genfromtxt(det_files[1], delimiter=',', skip_header=0, names=['id', 'x', 'y'])

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
			# print("Match! Deep {} ({}), Shallow {} ({})".format(d_id, d_loc, s_id, s_loc))
			shallow_match.append(s_id)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.plot(deep_data['x'], deep_data['y'], 'o')
# ax.plot(shallow_data['x'], shallow_data['y'], 'x')

to_plot_ids = []
to_plot_xs = []
to_plot_ys = []

for i in range(len(shallow_data['id'])):
	if int(shallow_data['id'][i]) not in to_remove:
		to_plot_ids.append(shallow_data['id'][i])
		to_plot_xs.append(shallow_data['x'][i])
		to_plot_ys.append(shallow_data['y'][i])

# write good shallow to a file
with open('good_shallow.csv', 'w') as f:
	for i, s_id in enumerate(to_plot_ids):
		f.write('{}\n'.format(int(s_id)))

with open('good_deep.csv', 'w') as f:
	for i, d_id in enumerate(deep_dict):
		f.write('{}\n'.format(int(d_id)))


ax.plot(to_plot_xs, to_plot_ys, 'x')

# for i in range(len(to_plot_ids['id'])):
# 	ax.annotate(str(int(shallow_data['id'][i])), (shallow_data['x'][i], shallow_data['y'][i]), size=7)

# for i in range(len(to_plot_ids)):
# 	ax.annotate(str(int(to_plot_ids[i])), (to_plot_xs[i], to_plot_ys[i]), size=7)

print(len(to_plot_xs))

# top down figure
ax.set_xlabel(r'X [m]', size=15)
ax.set_ylabel(r'Y [m]', size=15)
# ax.set_xlim([-2.5, 2.5])
ax.set_aspect('equal')
ax.tick_params(labelsize=15)
# ax.legend(loc='lower left')
plt.tight_layout()
fig.savefig('top_down.png', dpi=300, edgecolor='none', bbox_inches='tight')
