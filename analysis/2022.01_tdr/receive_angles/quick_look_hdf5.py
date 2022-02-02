import numpy as np
import matplotlib
from matplotlib import pyplot as plt
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

# files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3/hex_shallowheavy_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV*_-0.5_*'
files = '/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3/hex_shallowheavy_array/config_ARZ2020_noise/D01detector_sim/e/e_18.00eV*.hdf5'

# filename = 'e_20.00eV_0.0_0.1.part000000.hdf5'
# filename = 'e_17.00eV_0.0_0.1.hdf5'
filenames = sorted(glob.glob(files))
all_thetas = []
max_amp_thetas = []
for f in filenames:
    temp_all_thetas, temp_max_amp_thetas = helper.dig_around(f, 'PA_4channel_100Hz', 'LPDA_2of4_100Hz',
        hybrid_list, shallow_list
    )
    if temp_all_thetas is not None:
        for t in temp_all_thetas:
            all_thetas.append(t)
    if temp_max_amp_thetas is not None:
        for t in temp_max_amp_thetas:
            max_amp_thetas.append(t)

all_thetas = np.rad2deg(all_thetas)
max_amp_thetas = np.rad2deg(max_amp_thetas)


fig = plt.figure()
ax = fig.add_subplot(111)
bins = np.linspace(0, 180, 180)
ax.hist(all_thetas, bins=bins, 
    histtype='step', alpha=0.75, 
    density=True,
    label='Channel 8, All Showers, All Rays')
ax.hist(max_amp_thetas, bins=bins, 
    histtype='step', alpha=0.75, 
    density=True,
    label='Max Amplitude Channel and Ray')
ax.set_title('NuE, 1E18')
ax.set_xlabel('Receive Angle (deg)')
ax.set_ylabel('PDF')
ax.legend()
fig.savefig('for_dave.png')