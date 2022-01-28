import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
import json
import os
import sys
import pickle
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections
import helper
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--det', required=True, help='which detector index')
parser.add_argument('--mode', required=True, help='which mode: deepshallow or hybridshallow')
args = parser.parse_args()

the_det = int(args.det)
the_mode = args.mode

detectors = [
    "baseline_array",
    "hex_hybrid_only_array",
    "hex_shallow_array",
    "hex_shallowheavy_array"
]

top = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3"
detector = detectors[the_det]
config = "config_ARZ2020_noise"
detsim = "D01detector_sim"
deep_trigger = 'PA_4channel_100Hz'
shallow_trigger = 'LPDA_2of4_100Hz'
mode = the_mode

do_review = False

flavors = [
    "e",
    "mu",
    "tau"
]
result = {}
for flavor in flavors:
    result[flavor] = {
                    'E' : [],
                    'total_veff': [],
                    'deeporhybrid_veff': [],
                    'shallow_veff': [],
                    'dual_veff': [],
                    'total_aeff': [],
                    'deeporhybrid_aeff': [],
                    'shallow_aeff': [],
                    'dual_aeff': [],
                    'n_thrown': [],
                    'trig_weight': []
                    }
    
    pkl_file_name = os.path.join('results/overlap_' + detector + "_deeptrig_" + deep_trigger + "_shallowtrig_" + shallow_trigger + "_mode_"+ mode+'_' + flavor + ".pkl")
    with open(pkl_file_name, "rb") as fin:
        coincidences = pickle.load(fin)
    
    for lgE, value in coincidences.items():
        result[flavor]['E'].append(lgE)
        veff_total = value['total_veff']
        veff_deeporhybrid = value['deeporhybrid_only_veff']
        veff_shallow = value['shallow_only_veff']
        veff_dual = value['dual_veff']
        
        lint = cross_sections.get_interaction_length(np.power(10., float(lgE)))
        aeff_total = veff_total/lint
        aeff_deeporhybrid = veff_deeporhybrid/lint
        aeff_shallow = veff_shallow/lint
        aeff_dual = veff_dual/lint

        # convert to the right units (I could be more compact than this, but want to be explicit)
        veff_total = veff_total * 4 * np.pi / units.km**3
        veff_deeporhybrid = veff_deeporhybrid * 4 * np.pi / units.km**3
        veff_shallow = veff_shallow * 4 * np.pi / units.km**3
        veff_dual = veff_dual * 4 * np.pi / units.km**3

        aeff_total = aeff_total * 4 * np.pi / units.km**2
        aeff_deeporhybrid = aeff_deeporhybrid * 4 * np.pi / units.km**2
        aeff_shallow = aeff_shallow * 4 * np.pi / units.km**2
        aeff_dual = aeff_dual * 4 * np.pi / units.km**2

        result[flavor]['total_veff'].append(veff_total)
        result[flavor]['deeporhybrid_veff'].append(veff_deeporhybrid)
        result[flavor]['shallow_veff'].append(veff_shallow)
        result[flavor]['dual_veff'].append(veff_dual)
        result[flavor]['total_aeff'].append(aeff_total)
        result[flavor]['deeporhybrid_aeff'].append(aeff_deeporhybrid)
        result[flavor]['shallow_aeff'].append(aeff_shallow)
        result[flavor]['dual_aeff'].append(aeff_dual)
        result[flavor]['n_thrown'].append(value['n_thrown'])
        result[flavor]['trig_weight'].append(value['trig_weight'])

energies = result['e']['E']
average_total_veff = np.zeros(9)
average_deeporhybrid_veff = np.zeros(9)
average_shallow_veff = np.zeros(9)
average_dual_veff = np.zeros(9)
average_total_aeff = np.zeros(9)
average_deeporhybrid_aeff = np.zeros(9)
average_shallow_aeff = np.zeros(9)
average_dual_aeff = np.zeros(9)
total_n_thrown = np.zeros(9)
total_trig_weight = np.zeros(9)
for iflavor, flavor in enumerate(flavors):
    for iE, energy in enumerate(energies):
        average_total_veff[iE]+=result[flavor]['total_veff'][iE]/3
        average_deeporhybrid_veff[iE]+=result[flavor]['deeporhybrid_veff'][iE]/3
        average_shallow_veff[iE]+=result[flavor]['shallow_veff'][iE]/3
        average_dual_veff[iE]+=result[flavor]['dual_veff'][iE]/3
        average_total_aeff[iE]+=result[flavor]['total_aeff'][iE]/3
        average_deeporhybrid_aeff[iE]+=result[flavor]['deeporhybrid_aeff'][iE]/3
        average_shallow_aeff[iE]+=result[flavor]['shallow_aeff'][iE]/3
        average_dual_aeff[iE]+=result[flavor]['dual_aeff'][iE]/3
        total_n_thrown[iE]+=result[flavor]['n_thrown'][iE]
        total_trig_weight[iE]+=result[flavor]['trig_weight'][iE]

if do_review:
    average_total_veff, average_deeporhybrid_veff, average_shallow_veff, average_dual_veff, average_total_aeff, average_deeporhybrid_aeff, average_shallow_aeff, average_dual_aeff = helper.get_review_array()
    detector = 'review array'
    deep_trigger='review'
    shallow_trigger='review'

fraction_deeporhybrid = average_deeporhybrid_veff/average_total_veff
fraction_shallow = average_shallow_veff/average_total_veff
fraction_dual = average_dual_veff/average_total_veff

if mode == 'deepshallow':
    sub1 = 'Deep Trigger'
    sub2 = 'Shallow Trigger'
elif mode == 'hybridshallow':
    sub1 = 'Hybrid Station'
    sub2 = 'Surface Stations'

output_csv = f'log10(energy [eV]), veff total [km^3 sr water equiv], veff {sub1} only, veff shallow only, veff coincidence, '
output_csv += f'aeff total [km^2 sr water equiv], aeff {sub1} only, aeff shallow only, aeff coincidence, '
output_csv += f'frac {sub1} only, frac shallow only, frac coincidence'
output_csv += "\n"
for iE, energy in enumerate(energies):
    output_csv += '{:.1f}, {:e}, {:e}, {:e}, {:e}, {:e}, {:e}, {:e}, {:e}, {:>.2f}, {:>.2f}, {:>.2f} \n'.format(
        float(energy), 
        average_total_veff[iE], average_deeporhybrid_veff[iE], average_shallow_veff[iE], average_dual_veff[iE],
        average_total_aeff[iE], average_deeporhybrid_aeff[iE], average_shallow_aeff[iE], average_dual_aeff[iE],
        fraction_deeporhybrid[iE], fraction_shallow[iE], fraction_dual[iE])
with open(f'results/veff_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}_mode_{mode}.csv', 'w') as fout:
    fout.write(output_csv)

output_csv_2 = 'energy, num thrown, total trig weight \n'
for iE, energy in enumerate(energies):
    output_csv_2 += '{:.1f}, {}, {} \n'.format(
        float(energy), total_n_thrown[iE], total_trig_weight[iE])
with open(f'results/stats_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}.csv', 'w') as fout2:
    fout2.write(output_csv_2)



fig, axs = plt.subplots(1, 2, figsize=(12,6))
colors = ['C0', 'C1', 'C2']
markers = ['o', 's', '^']
styles = ['C0o-', 'C1s--', 'C2^-.', 'C3v:']
xx = result[flavor]['E']
fig.suptitle(f"{detector}")

axs[0].plot(xx, average_deeporhybrid_aeff+average_shallow_aeff+average_dual_aeff, styles[3], label='Sum')
axs[0].plot(xx, average_deeporhybrid_aeff, styles[0], label=f'{sub1} component')
axs[0].plot(xx, average_shallow_aeff, styles[1], label=f'{sub2} component')
axs[0].plot(xx, average_dual_aeff, styles[2], label=f'{sub1} + {sub2} coincidence')
axs[0].set_yscale('log')
axs[0].set_xlabel("log10(energy [eV])")
axs[0].set_ylabel(r"[km$^2$ * str]")
axs[0].set_title("Water Equivalent Effective Area ")
axs[0].set_ylim([1E-5,1E2])
axs[0].legend(loc='lower right')


axs[1].plot(xx, fraction_deeporhybrid, styles[0], label=f'{sub1} component')
axs[1].plot(xx, fraction_shallow, styles[1], label=f'{sub2} component')
axs[1].plot(xx, fraction_dual, styles[2], label=f'{sub1} + {sub2} coincidence')
axs[1].plot(xx, fraction_deeporhybrid+fraction_shallow+fraction_dual, styles[3], label='Sum')
axs[1].set_ylim([0, 1.1])
axs[1].set_xlabel("log10(energy [eV])")
axs[1].set_ylabel("Fraction")
axs[1].set_title("Fraction of the All-Sky Effective Area")
fig.tight_layout(pad=2)
outfilename = f'plots/veff_fractions_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}_mode_{mode}.png'
fig.savefig(outfilename)