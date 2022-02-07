from fileinput import filename
from re import A
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import h5py
import glob
import os
import sys
import pickle
from multiprocessing import Pool, pool
from functools import partial
import helper
import argparse

detector = 'hex_shallowheavy_array'
hybrid_list = np.genfromtxt(f"station_lists/stations_{detector}_hybrid.csv")
shallow_list = np.genfromtxt(f"station_lists/stations_{detector}_shallow.csv")



# files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3/hex_shallowheavy_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV*_-0.1_*.nur'
# files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3/hex_shallowheavy_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV*.hdf5'
# filenames = sorted(glob.glob(files))

files = 'e_20.00eV_0.0_0.1.part000000.nur.tar.gz'

all_thetas = []
all_weights = []
max_amp_thetas = []
max_amp_weights = []
deep_trigger = 'PA_4channel_100Hz'
shallow_trigger = 'LPDA_2of4_100Hz'
the_trigger = deep_trigger

local_func = partial(helper.parallel_process, the_trigger=the_trigger)

files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step2/baseline_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV_*/*.nur*'
# files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step2/baseline_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV_0.0*/*00000*.nur*'
filenames = sorted(glob.glob(files))
print("Num files: {}".format(filenames))
n_cores = 10

with Pool(n_cores) as p:
    pool_result = p.map(local_func, filenames)

for result in pool_result:
    if result is None:
        continue
    all_thetas += result['all_thetas']
    all_weights += result['all_weights']
    max_amp_thetas += result['max_amp_thetas']
    max_amp_weights += result['max_amp_weights']

all_thetas = np.rad2deg(all_thetas)
max_amp_thetas = np.rad2deg(max_amp_thetas)
all_weights = np.asarray(all_weights)
max_amp_weights = np.asarray(max_amp_weights)

if 'PA' in the_trigger:
    for_plot = 'Ch 8'
elif 'LPDA' in the_trigger:
    for_plot = 'Ch 0'

fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(111)
bins = np.linspace(0, 180, 180)
ax.hist(all_thetas, bins=bins, 
    weights=all_weights,
    histtype='step', alpha=0.75, 
    density=True,
    label='{}, All Showers, All Rays (w/ weights)'.format(the_trigger))
ax.hist(all_thetas, bins=bins, 
    histtype='step', alpha=0.75, 
    linestyle='--',
    density=True,
    label='{}, All Showers, All Rays (no weights)'.format(the_trigger))
ax.hist(max_amp_thetas, bins=bins, 
    weights = max_amp_weights,
    histtype='step', alpha=0.75, 
    density=True,
    label='Max Amp Channel and Ray (w/ weights)')
ax.hist(max_amp_thetas, bins=bins, 
    histtype='step', alpha=0.75, 
    linestyle='--',
    density=True,
    label='Max Amp Channel and Ray (no weights)')
ax.set_title('NuE, 1E18')
ax.set_xlabel('Receive Angle (deg)')
ax.set_ylabel('PDF')
ax.legend(bbox_to_anchor=(1.05, 1.0))
plt.tight_layout()
fig.savefig('recang_{}.png'.format(the_trigger))

# del fig, ax

# cmap=plt.cm.plasma
# fig = plt.figure(figsize=(14,6))
# ax = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
# bins = [np.linspace(0,180,180), np.linspace(0,2.2,220)]

# counts, xedges, yedges, im = ax.hist2d(
#     all_thetas,
#     all_ffs,
#     bins=bins,
#     cmap=cmap,
#     norm=colors.LogNorm(),
#     cmin=1
# )
# cbar = plt.colorbar(im, ax=ax)
# cbar.set_label('Counts')
# ax.set_title('NuE, 1E18')
# ax.set_xlabel('Receive Angle (deg)')
# ax.set_ylabel('Focusing Factor')
# ax.set_title('{}, All Showers, All Ray'.format(for_plot))


# counts, xedges, yedges, im = ax2.hist2d(
#     max_amp_thetas,
#     max_amp_ffs,
#     bins=bins,
#     cmap=cmap,
#     norm=colors.LogNorm(),
#     cmin=1
# )
# cbar2 = plt.colorbar(im, ax=ax2)
# cbar2.set_label('Counts')
# ax2.set_title('NuE, 1E18')
# ax2.set_xlabel('Receive Angle (deg)')
# ax2.set_ylabel('Focusing Factor')
# ax2.set_title('Max Amp Shower/Channel/Ray')

# plt.tight_layout()
# fig.savefig('ffs_{}.png'.format(the_trigger))
