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
from NuRadioReco.utilities import units
from NuRadioMC.utilities.Veff import get_Veff_water_equivalent as gwe
import helper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--det', required=True, help='which detector index')
parser.add_argument('--mode', required=True, help='which mode: deepshallow or hybridshallow')
args = parser.parse_args()

the_det = int(args.det)
the_mode = args.mode

top = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3"
detectors = [
    "baseline_array",
    "hex_hybrid_only_array",
    "hex_shallow_array",
    "hex_shallowheavy_array"
]

detector = detectors[the_det]
config = "config_ARZ2020_noise"
detsim = "D01detector_sim"
path=os.path.join(top, detector, config, detsim)

deep_trigger = 'PA_4channel_100Hz'
shallow_trigger = 'LPDA_2of4_100Hz'
mode = the_mode
hybrid_list = np.genfromtxt(f"../station_lists/stations_{detector}_hybrid.csv")
shallow_list = np.genfromtxt(f"../station_lists/stations_{detector}_shallow.csv")

flavors = [
    "e",
    "mu",
    "tau"
]

zen_bins = np.linspace(-1,1,21)
coszen_to_bin = {}
for iZ, czen1 in enumerate(zen_bins[:-1]):
    coszen_to_bin[f"{czen1:.1f}"] = iZ
logEs = np.arange(16, 20.1, 0.5)
n_cores = 15

local_func = partial(helper.tmp_advanced, 
    hybrid_list=hybrid_list, 
    shallow_list=shallow_list,
    deep_trigger=deep_trigger,
    shallow_trigger=shallow_trigger,
    )

for flavor in flavors:
    total_veff = {}
    for logE in logEs:
        total_veff[f"{logE:.1f}"] = {}
        num_zen_bins = 20

        the_list = ['total', 'hd', 'hs', 'ss', 'hd_hs', 'hd_ss', 'hs_ss', 'hd_hs_ss']
        all_sky = {}
        binned = {}
        for l in the_list:
            all_sky[l] = 0
            binned[l] = np.zeros(20)
             
        print("Flavor {}, logE {}".format(flavor, logE))

        local_path = os.path.join(path, f"{flavor}/{flavor}_{logE:.2f}*.hdf5")
        filenames = glob.glob(local_path)
        print("Filenames {}".format(filenames))

        with Pool(n_cores) as p:
            pool_result = p.map(local_func, filenames)
        
        for result in pool_result:
            if result is None:
                continue
                
            czmin = str('{:.1f}'.format(result['czmin']))
            zen_bin = coszen_to_bin[czmin]

            n_events = result['n_events']
            volume = result['volume']

            for l in the_list:
                all_sky[l] += result[l+'_weight']/n_events * volume
                binned[l][zen_bin] += result[l+'_weight']/n_events * volume

        for l in the_list:
            total_veff[f"{logE:.1f}"][l] = gwe(all_sky[l]/num_zen_bins)
            total_veff[f"{logE:.1f}"][l+'_zen_bins'] = gwe(binned[l])
        
        total_veff[f"{logE:.1f}"]['czmins'] = zen_bins[:-1]

    pkl_file_name = os.path.join('results/overlap_' + detector + "_deeptrig_" + deep_trigger + "_shallowtrig_" + shallow_trigger + "_mode_"+ mode+'_' + flavor + ".pkl")
    with open(pkl_file_name, "wb") as fout:
        pickle.dump(total_veff, fout, protocol=4)