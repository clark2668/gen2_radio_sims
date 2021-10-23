import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

import helper as helper
import copy

gen2_optical = helper.get_string_heads('IceCubeHEX_Sunflower_240m_v3_ExtendedDepthRange.GCD.txt.gz')
sectors = helper.get_sectors()

doJVS = False
if doJVS:
	# radio_jvs = helper.half_fantasy_radio_geometry(sectors['Dark Sector'], 
	# 	spacing=2E3, nstations=nstations)
	# xv, yv = radio_jvs[:,0], radio_jvs[:,1]
	# R = 2
	# ratio = R * np.sqrt(3)/2 # sqrt(3)/2 = sin(pi/3) (height of the equilateral triangle in the hexagon)
	# yv = yv * R
	# xv = xv * ratio
	# xv[::2] += ratio/2
	# ax.plot(radio_jvs[:,0], radio_jvs[:,1], 'o', markersize=2)
    print('yolo')

spacing = 1.5
nstations = 1000

doHEX = False
if doHEX:

	# deep
	spacing = 2E3
	radio_x, radio_y = helper.get_hex_grid(nstations,spacing)
	radio_x -= (np.sqrt(400)) * spacing
	radio_y -= np.sqrt(400)/2 * spacing
	new_x, new_y = helper.trim_to_fit(radio_x, radio_y)

	# # shallow
	# nstations = 4000
	# radio_x_2, radio_y_2 = helper.get_hex_grid(nstations,spacing)
	# radio_x_2 -= (np.sqrt(nstations/2)) * spacing
	# radio_y_2 -= np.sqrt(nstations/2)/2 * spacing
	# new_x_2, new_y_2 = helper.trim_to_fit(radio_x_2, radio_y_2)
	# # new_x_2_spacing = new_x_2[10] = new_x_2[9]
	# # new_y_2_spacing = new_y_2[10] = new_y_2[9]
	# new_x_2 = np.asarray(new_x_2)
	# new_y_2 = np.asarray(new_y_2)

	ratio = spacing * np.sqrt(3)/2 # sqrt(3)/2 = sin(pi/3) (height of the equilateral triangle in the hexagon)
	# new_x_2 = new_x - ratio/2
	new_x_2 = copy.deepcopy(new_x) #  - ratio/2
	new_x_2 -= ratio/2
	# new_x_2[::2] -= ratio/2
	new_y_2 = new_y - spacing/2

	new_x_2, new_y_2 = helper.trim_to_fit(new_x_2, new_y_2)


doRECT = True
if doRECT:

    shift = 0

    xx_deep = np.arange(-44, 44.1, spacing)*1000.
    yy_deep = np.arange(-44, 44.1, spacing)*1000.
    d = np.meshgrid(xx_deep, yy_deep)
    xx_deep = d[0].flatten() + shift
    yy_deep = d[1].flatten() + shift

    xx_shallow = np.arange(-44 - 0.5 * spacing, 44.1 + 0.5 * spacing, spacing)*1000.
    yy_shallow = np.arange(-44 - 0.5 * spacing, 44.1 + 0.5 * spacing, spacing)*1000.
    s = np.meshgrid(xx_shallow, yy_shallow)
    xx_shallow = s[0].flatten() + shift
    yy_shallow = s[1].flatten() + shift

    xx_deep_rot = []
    yy_deep_rot = []
    xx_shallow_rot = []
    yy_shallow_rot = []

    for x, y in zip(xx_shallow, yy_shallow):
        x1, y1 = helper.rotate_point(x,y,0,0,4)
        xx_shallow_rot.append(x1)
        yy_shallow_rot.append(y1)

    for x, y in zip(xx_deep, yy_deep):
        x1, y1 = helper.rotate_point(x,y,0,0,4)
        xx_deep_rot.append(x1)
        yy_deep_rot.append(y1)

    xx_deep_trim, yy_deep_trim = helper.trim_to_fit(xx_deep_rot, yy_deep_rot)
    xx_shallow_trim, yy_shallow_trim = helper.trim_to_fit(xx_shallow_rot, yy_shallow_rot)

    print("N Deep + Shallow {}".format(len(xx_deep_trim)))
    print("N Shallow only {}".format(len(xx_shallow_trim)))

fig, ax = plt.subplots(figsize=(7,5))
ax.set_xlabel('X [m]', fontsize=15)

for name, sector in sectors.items():
    color, alpha = helper.sectorColors[name]
    ax.fill(sector.T[0],sector.T[1],
            facecolor=color, alpha=alpha, edgecolor='none',
            label=name,zorder=5)

ax.plot(gen2_optical['x'], gen2_optical['y'], 's', markersize=1)

# ARA_x, ARA_y = helper.get_ARA()
# ax.plot(ARA_x, ARA_y, 'd', color='firebrick', label='ARA', markersize=2)

# ax.plot(xx_shallow, yy_shallow, 'o', markersize=2, label='Shallow only')
ax.plot(xx_shallow_trim, yy_shallow_trim, 'o', markersize=2, label='Shallow only ({})'.format(len(xx_shallow_trim)))
ax.plot(xx_deep_trim, yy_deep_trim, 'o', markersize=2, label='Deep + Shallow ({})'.format(len(xx_deep_trim)))


# ax.set_xlim(-5000,1000)
# ax.set_ylim(-3000,4000)
ax.set_ylabel('Y [m]', fontsize=15)
ax.tick_params(axis='both', labelsize=15)
ax.set_aspect('equal')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
fig.savefig('geometry.png', dpi=300)


top = sectors['Dark Sector'][2:4]
print(top)
top_1 = top[0]
top_2 = top[1]
top_vec = np.asarray([top_2[0] - top_1[0], top_2[1] - top_1[1]])
print(top_vec)
top_vec = top_vec/np.linalg.norm(top_vec)
print('----')

bottom = sectors['Dark Sector'][0:2]
print(bottom)

bottom_1 = bottom[0]
bottom_2 = bottom[1]
bottom_vec = np.asarray([bottom_1[0] - bottom_2[0], bottom_1[1] - bottom_2[1]])
print(bottom_vec)

bottom_vec = bottom_vec/np.linalg.norm(bottom_vec)

# ang = np.rad2deg(np.arccos())
# ang = np.dot(top_vec, bottom_vec)
ang = np.rad2deg(np.arccos(top_vec[0]*bottom_vec[0] + top_vec[1]*bottom_vec[1]))
print("Ang is {}".format(ang))