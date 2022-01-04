import numpy as np
import os

from NuRadioReco.utilities import units
import helper as hp


det_files = [
    "baseline_array",
    "hex_hybrid_only_array",
    "hex_shallow_array",
    "hex_shallowheavy_array"
]

config_file = "config_ARZ2020_noise"
sim_file = "D01detector_sim"

for det_file in det_files:

    coszenbins = hp.get_coszenbins()
    logEs = hp.get_logEs()
    energies = 10 ** logEs * units.eV
    flavors = [
        "e", 
        "mu", 
        "tau"
        ]

    do_sim_output_dir = False
    if(do_sim_output_dir):

        base_dir = "/data/sim/Gen2/radio/2020/gen2-tdr-2021/simulation_output"

        step2dir = os.path.join(base_dir, f"secondaries_1700km2", f"{det_file}", f"{config_file}", f"{sim_file}")
        if(not os.path.exists(step2dir)):
            os.makedirs(step2dir)

        for flavor in flavors:
            for iE in range(len(logEs)):
                for iC in range(len(coszenbins) - 1):
                    czen1 = coszenbins[iC]
                    czen2 = coszenbins[iC + 1]
                    E = energies[iE]
                    pattern = f"{flavor}_{logEs[iE]:.2f}eV_{czen1:.1f}_{czen2:.1f}"
                    print(pattern)
                    folder = os.path.join(step2dir, flavor, f"{pattern}")
                    if(not os.path.exists(folder)):
                        os.makedirs(folder)
    
    do_scratch_output_dir = False
    if(do_scratch_output_dir):

        hostname = os.uname().nodename
        if 'sub-1' not in hostname:
            print("You are trying to make scratch directories, but are on the {} system.".format(hostname))
            print("This is probably incorret. Switch to sub-1!")
            raise RuntimeError

        print("Making scratch dirs")

        scratch_basedir = "/scratch/brianclark/gen2radiosims/trash/"

        for flavor in flavors:
            print("  Working on flavor {}".format(flavor))

            scratchdir = os.path.join(scratch_basedir, f"{det_file}", f"{flavor}", "log")
            print("    Scratch dir will be {}".format(scratchdir))
            if(not os.path.exists(scratchdir)):
                os.makedirs(scratchdir)
            scratchdir = os.path.join(scratch_basedir, f"{det_file}", f"{flavor}", "err")
            if(not os.path.exists(scratchdir)):
                os.makedirs(scratchdir)
            scratchdir = os.path.join(scratch_basedir, f"{det_file}", f"{flavor}", "out")
            if(not os.path.exists(scratchdir)):
                os.makedirs(scratchdir)
