# ax.plot(gen2_optical['x'], gen2_optical['y'], 'o', markersize=2)

# for name, sector in sectors.items():
#     color, alpha = helper.sectorColors[name]
#     ax.fill(sector.T[0],sector.T[1],
#             facecolor=color, alpha=alpha, edgecolor='none',
#             label=name,zorder=5)

# x, y = np.random.normal(size=(2, 10000))
# im = ax.hexbin(x, y, gridsize=20)
# paths = im.get_paths()
# offs = im.get_offsets()
# print(offs)
# print(paths)

def get_hexagon_points(n, m):
	x_vals = []
	y_vals = []
	x_vals.append(3*n + 1)
	x_vals.append(3*n - 1)
	y_vals.append(m*np.sqrt(3))
	y_vals.append(m*np.sqrt(3))

	x_vals.append(3*n + 0.5)
	y_vals.append((m+0.5)*np.sqrt(3))

	x_vals.append(3*n + 0.5)
	y_vals.append((m-0.5)*np.sqrt(3))

	x_vals.append(3*n - 0.5)
	y_vals.append((m-0.5)*np.sqrt(3))

	x_vals.append(3*n - 0.5)
	y_vals.append((m+0.5)*np.sqrt(3))

	return x_vals, y_vals


### kinda works
N = 144
R = 2000
ratio = R * np.sqrt(3)/2 # sqrt(3)/2 = sin(pi/3) (height of the equilateral triangle in the hexagon)

N_X = int(np.sqrt(N))
N_Y = N // N_X
xv, yv = np.meshgrid(np.arange(N_X), np.arange(N_Y), sparse=False, indexing='xy')

yv = yv * R
xv = xv * ratio
xv[::2, :] += ratio/2

new_x = []
new_y = []
for xs, ys in zip(xv, yv):
	for x, y in zip(xs, ys):
		new_x.append(x)
		new_y.append(y)

ax.plot(new_x, new_y, 'o')
