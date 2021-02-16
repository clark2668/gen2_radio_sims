import json
import copy
import numpy as np
from matplotlib import pyplot as plt
from NuRadioReco.utilities import units

spacing = 2.0  # in km
xx = []
yy = []
station_id = 0
xx = np.arange(-11, 11.1, spacing) * units.km
yy = np.arange(-11, 11.1, spacing) * units.km

spacing_s = 2
xx_s = np.arange(-11 - 0.5 * spacing_s, 11.1 + 0.5 * spacing_s, spacing_s) * units.km
yy_s = np.arange(-11 - 0.5 * spacing_s, 11.1 + 0.5 * spacing_s, spacing_s) * units.km

print('Num deep stations {}'.format(len(xx)*len(yy)))
print("Num independent shallow stations {}".format(len(xx_s)*len(yy_s)))

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
fig.savefig("review_array_layout.png", dpi=300)
