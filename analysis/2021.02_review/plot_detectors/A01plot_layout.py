import json
import copy
import numpy as np
from matplotlib import pyplot as plt
from NuRadioReco.utilities import units

spacing = 2.0  # in km
xx = []
yy = []
station_id = 0
xx = np.arange(-10, 10.1, spacing) * units.km
yy = np.arange(-12.5, 12.51, spacing) * units.km

spacing_s = 2
xx_s = np.arange(-10 - 0.5 * spacing_s, 10.1 + 0.5 * spacing_s, spacing_s) * units.km
yy_s = np.arange(-12.5 - 0.5 * spacing_s, 12.51 + 0.5 * spacing_s, spacing_s) * units.km

print(f"generates {station_id} stations with a spacing of {spacing}km")
print(f"deep + shallow: {len(xx)} x {len(yy)} = {len(xx) * len(yy)} stations with {spacing} spacing")
print(f"shallow only: {len(xx_s)} x {len(yy_s)} = {len(xx_s) * len(yy_s)} stations with {spacing_s} spacing -> effective shallow spacing {2**0.5 * 0.5 * spacing:.2f}")

d = np.meshgrid(xx, yy)
xxx = d[0].flatten()
yyy = d[1].flatten()

d = np.meshgrid(xx_s, yy_s)
xxx_s = d[0].flatten()
yyy_s = d[1].flatten()

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.plot(xxx / units.km, yyy / units.km, "C0o", label='Deep + Shallow Detector', markersize=5)
ax.plot(xxx_s / units.km, yyy_s / units.km, "C1D", label='Shallow Only Detector', markersize=3)
ax.set_xlabel("X [km]")
ax.set_ylabel("Y [km]")
ax.set_aspect("equal")
ax.legend(bbox_to_anchor=(0.1, 1.05))
fig.tight_layout()
fig.savefig("review_array.png", dpi=300)
