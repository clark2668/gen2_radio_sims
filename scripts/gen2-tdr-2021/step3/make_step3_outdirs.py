import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp

step1dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_input/secondaries_1700km2/step1/"
step2dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/"
base_dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output/secondaries_1700km2/step3"

det_files = [
    "baseline_array",
    "hex_hybrid_only_array",
    "hex_shallow_array",
    "hex_shallowheavy_array"
]

config_file = "config_ARZ2020_noise"
sim_file = "D01detector_sim"

for det_file in det_files:

    do_sim_output_dir = False
    if(do_sim_output_dir):

        step3dir = os.path.join(base_dir, f"{det_file}", f"{config_file}", f"{sim_file}")
        if(not os.path.exists(step3dir)):
            os.makedirs(step3dir)

        coszenbins = hp.get_coszenbins()
        logEs = hp.get_logEs()
        energies = 10 ** logEs * units.eV

        flavors = ["e", "mu", "tau"]

        for flavor in flavors:
            folder = os.path.join(step3dir, flavor)
            if(not os.path.exists(folder)):
                os.makedirs(folder)
