import matplotlib.pyplot as plt
import numpy as np

import helper as helper

gen2_optical = helper.get_string_heads('IceCubeHEX_Sunflower_240m_v3_ExtendedDepthRange.GCD.txt.gz')
sectors = helper.get_sectors()

#################
# make up a geometry
#################

spacing = 1.5
nstations = 1000
    
# make a big rectangular grid of stations, one for deep and one for shallow
# these will extend outside the dark sector by a lot. we will trim them down later.
xx_deep = np.arange(-44, 44.1, spacing)*1000.
yy_deep = np.arange(-44, 44.1, spacing)*1000.
d = np.meshgrid(xx_deep, yy_deep)
xx_deep = d[0].flatten()
yy_deep = d[1].flatten()

xx_shallow = np.arange(-44 - 0.5 * spacing, 44.1 + 0.5 * spacing, spacing)*1000.
yy_shallow = np.arange(-44 - 0.5 * spacing, 44.1 + 0.5 * spacing, spacing)*1000.
s = np.meshgrid(xx_shallow, yy_shallow)
xx_shallow = s[0].flatten()
yy_shallow = s[1].flatten()

# rotate the points by four degrees (because it aligns them a bit better with axis somehow)
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

# cut out any parts of the array that don't fit in the dark sector wedge
xx_deep_trim, yy_deep_trim = helper.trim_to_fit(xx_deep_rot, yy_deep_rot)
xx_shallow_trim, yy_shallow_trim = helper.trim_to_fit(xx_shallow_rot, yy_shallow_rot)

#################
# plots
#################

fig, ax = plt.subplots(figsize=(7,5))
ax.set_xlabel('X [m]', fontsize=15)

# plot all the sectors (dark sector, clean air sector, etc.)
for name, sector in sectors.items():
    color, alpha = helper.sectorColors[name]
    ax.fill(sector.T[0],sector.T[1],
            facecolor=color, alpha=alpha, edgecolor='none',
            label=name,zorder=5)

# plot Gen2 optical
ax.plot(gen2_optical['x'], gen2_optical['y'], 's', markersize=1)

# and our candidate radio array
ax.plot(xx_shallow_trim, yy_shallow_trim, 'o', markersize=2, label='Shallow only ({})'.format(len(xx_shallow_trim)))
ax.plot(xx_deep_trim, yy_deep_trim, 'o', markersize=2, label='Deep + Shallow ({})'.format(len(xx_deep_trim)))

# you can also add ARA, in case the reference is helpful
# ARA_x, ARA_y = helper.get_ARA()
# ax.plot(ARA_x, ARA_y, 'd', color='firebrick', label='ARA', markersize=2)

# and the one Jakob had in the white paper
# radio_jvs = helper.half_fantasy_radio_geometry(sectors['Dark Sector'], 
# 	spacing=2E3, nstations=nstations)
# ax.plot(radio_jvs[:,0], radio_jvs[:,1], 'o', markersize=2)

ax.set_ylabel('Y [m]', fontsize=15)
ax.tick_params(axis='both', labelsize=15)
ax.set_aspect('equal')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
fig.savefig('geometry.png', dpi=300)
