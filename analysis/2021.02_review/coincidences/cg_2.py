import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
from scipy import interpolate
import json
import os
import sys
from radiotools import plthelpers as php

from NuRadioReco.utilities import units
from NuRadioReco.detector import detector
from scipy import integrate
from NuRadioMC.utilities import fluxes
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
from scipy import interpolate as intp
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import coordinates as coord
from NuRadioMC.utilities import cross_sections
from astropy.time import Time
from astropy.time import TimeDelta
import astropy.units as u
import pickle
import yaml
# plt.switch_backend('agg')

dist = 2
depth = 100

path = f"results/coincidences/run_input_500km2_01_dipoles_RNOG_{depth:.0f}m_{dist:.2f}km_config_Alv2009_nonoise_100ns_D02single_dipole_250MHz_output_run_input_500km2_01_surface_4LPDA_1dipole_RNOG_{0.5*dist:.2f}km_config_Alv2009_nonoise_100ns_D01surface_4LPDA_1dipole_250MHz_output_.pkl"
trigger_names = ['dipole_2.5sigma', 'dipole_1.5sigma']
result = {}
for tname in trigger_names:
    result[tname] = {'E': [],
                     'c2': [],
                     'c3': [],
                     'c4': [],
                     'c2_deep': [],
                     'c2_shallow': [],
                     'c2_deep_shallow': [], }

with open(path, "rb") as fin:
    coincidences = pickle.load(fin)

    print(f"trigger names {trigger_names}")
    for lgE, value in coincidences.items():
        for tname in trigger_names:
            result[tname]['E'].append(lgE)
        print(f"E = 10^{lgE}eV")
        for i in range(2, 5):
            output = f"\t>= {i} station coincidences: "
            for tname in trigger_names:
                n_stations = np.array(value[tname])
                n_stations1 = np.array(coincidences[lgE]["1"][tname])
                n_stations2 = np.array(coincidences[lgE]["2"][tname])
#                 n_stations_dual = (n_stations1 >= i) & (n_stations2 >= i)
                n_tot = np.sum(n_stations > 0)
                weights = np.array(coincidences[lgE]['weights'])
                fraction = np.sum(n_stations >= i) / n_tot
                fraction_w = np.sum(weights[n_stations >= i]) / np.sum(weights[n_stations > 0])
                fraction_w_1 = np.sum(weights[n_stations1 >= i]) / np.sum(weights[n_stations1 > 0])
                fraction_w_2 = np.sum(weights[n_stations2 >= i]) / np.sum(weights[n_stations2 > 0])
                fraction_w_dual = np.sum(weights[(n_stations1 >= 1) & (n_stations2 >= 1)]) / np.sum(weights[n_stations > 0])
                print(f"{np.sum(n_stations>=2)}/{np.sum(n_stations > 0):.1f}, {np.sum(n_stations2>=1)}/{np.sum(n_stations1 > 0):.1f}, {np.sum(n_stations2>=2)}/{np.sum(n_stations2 > 0):.1f} {np.sum(n_stations2>=1)+ np.sum(n_stations2>=2)}")
                print(f"{np.sum(weights[n_stations>=2]):.1f}/{np.sum(weights[n_stations > 0]):.1f}, {np.sum(weights[n_stations1>=2]):.1f}/{np.sum(weights[n_stations1 > 0]):.1f}, {np.sum(weights[n_stations2>=2]):.1f}/{np.sum(weights[n_stations2 > 0]):.1f} {np.sum(n_stations1>=1)+ np.sum(n_stations2>=1)}")
                output += f"\t{fraction*100:.1f}% ({fraction_w*100:.2f}%), dual = {fraction_w_dual* 100:.2f}%, , 1 = {fraction_w_1* 100:.2f}%, , 2 = {fraction_w_2* 100:.2f}%"
#                 output += f"\t{fraction_w*100:.1f}% ({fraction*100:.1f}%)"
                result[tname][f'c{i}'].append(fraction_w)
                if(i == 2):
                    result[tname][f'c{i}_deep'].append(fraction_w_1)
                    result[tname][f'c{i}_shallow'].append(fraction_w_2)
                    result[tname][f'c{i}_deep_shallow'].append(fraction_w_dual)
            print(output)

fig, ax = plt.subplots(1, 1)
tname = "dipole_1.5sigma"
title = f"hybrid with {depth:.0f}m deep at {dist:.1f}km + shallow (15m) at {dist/2:.1f}km, 1.5 sigma trigger level"
xx = result[tname]['E']
linestyles = ["-", "--", ":", "-."]
ax.plot(xx, result[tname]['c2'], php.get_color_linestyle(0) + php.get_marker_only(0), label=f'>= 2 stations')
ax.plot(xx, result[tname]['c2_deep'], php.get_color_linestyle(1) + php.get_marker_only(1), label=f'>= 2 stations {depth}m depth')
ax.plot(xx, result[tname]['c2_shallow'], php.get_color_linestyle(2) + php.get_marker_only(2), label=f'>= 2 stations 15m depth')
ax.plot(xx, result[tname]['c2_deep_shallow'], php.get_color_linestyle(3) + php.get_marker_only(3), label=f'shallow + deep coincidences')
ax.set_title(title)
ax.set_ylim(0, 1)
ax.set_xlabel("log10(energy [eV])")
ax.set_ylabel("coincidence rate")
ax.legend()
fig.tight_layout()
fig.savefig(f"plots/coincidences/{os.path.basename(path)}_{tname}.png")
plt.show()
