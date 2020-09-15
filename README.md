# Gen2 Radio Simulations
repository for gen2 radio sims stuff

- [Overview](#overview)
- [Simulation Tools and Steps](#simulation-tools-and-steps)
 * [pytools](#pytools)
 * [step 0](#step-0)
 * [step 1](#step-1)
 * [step 2](#step-2)
 * [step3](#step3)
* [Logistical Details](#logistical-details)
  + [Setting up the software](#setting-up-the-software)
  + [Submitting jobs](#submitting-jobs)
  + [git maintenance](#git-maintenance)

## Overview

The strategy for the simulation requires a few stages:

- step 0: create the configuration files for how to distribute the vertices, zeniths, azimuths, energies, etc of incident neutrinos
- step 1: generate a list of energy depositions in the ice based on the neutrino primaries from step 0 (from neutrino primary interactions, but also secondary interactions like pair production, etc. in the case of electron and muon neutrinos)
- step 2: propagate radio emission from the energy depositions in step 1 to a simulated station
- step 3: combine all of the small "output" files into a single main file

The simulation inputs, Step 0 and 1, are defined by input configuration names such as `secondaries_500km2`, which suggest that secondaries are enabled and vertices are tracked over a 500km2 volume.

The simulation outputs, Step 2 and 3, are defined by a combination of:
1. a geometry specification (how antennas are distributed in the ice, etc.), defined in a `.json` file
2. a configuration specification (what Askaryan and ice model to use, etc)  defined in a `.yaml` file
3. a simulation configuration (what triggers to run, etc.) defined in a `.py` file.
The outputs need to be organized according to these three specification files.

Because the inputs (step 0 and 1) are totally separable from the outputs (step 2 and 3), they should be stored in a separate directory. The structure used is below:

```
simulation_input
     secondaries_500km2
          step0
               e
               mu
               tau
          step1
               e
               mu
               tau
simulation_output
     secondaries_500km2
          geometry_specification
               configuration_specification
                    simulation_specification
                         e
                         mu
                         tau
```

We are also running the simulation in specific zenith bands, and so for each `e`, `mu`, and `tau` folder, there is a zenith band folder, e.g.: `e_18.50eV_-0.2_0.1` for electron neutrinos, of primary energy 18.50eV, and zeniths drawn from the range -0.2 to -0.1.

Simulations are generated in "parts"--that is, for a given flavor, energy bin, and zenith bin, there might be 10 "parts" which must be run in parallel, and then merged in step 3.

## Simulation Tools and Steps

### pytools
There is a small "helper" class in the `pytools` directory. This standardizes things like the zenith binning, energy binning, etc. To use it, you will need to do:

`export PYTHONPATH=/path/to/pytools:$PYTHONPATH`

### step 0
Step 0 is where we output the "control" `.py` files for NuRadioMC that tell NuRadioMC how to distribute the neutrinos that will become the step 1 files. This includes the neutrino energy, zeniths, vertex volume, etc. Run this by doing:

`python make_step0_files.py`

The main parameter, which sits near the top of the file, is the `base_dir`, which is where you ant the step 0 and step 1 files to be placed.

### step 1
Step 1 is the process where we actually run the `.py` control files created in step 0 to generate the list of energy depositions. Running `python make_step1_dag.py` will generate the three dagman files (one for each flavor), which can then be submitted by doing `condor_submit_dag dagman_step1_e.dag`.

The main parameters, which sit near the top of the dag maker, is `step0dir` and `step1dir`.

### step 2
Step 2 is the process where we run NuRadioMC on the list of energy depositions created in step 1.

To make the output directory structure for a corresponding geometry, configuration, and simulation specification, run `python make_step2_outdirs.py`

To make the dagman files, do `python make_step2_dag.py`. The major variables to be changed here (as well as in the output directory maker above) is `step1dir`, `step2dir`, `det_file` (the detector json file), `config_file` (the config yaml file), and the `sim_file` (the simulation .py file).

Then you can submit the per flavor simulations by doing `condor_submit_dag dagman_step2_e.dag`.

### step3
After all of step 2 is complete, there is a final step which will merge all of the step 2 files in a single zenith bin into a "total" file. The naming convention is `filename.hdf5.partXXXXXX`. If you save them as `filename.partXXXXXX.hdf5`, then `rename.sh` is provided to change the order of the final two parts if you save them differently which was done early during production.

Do `python make_step3_dag.py` to make dag file which can then be submitted by `condor_submit_dag dagman_step3.py`. Note that this step (and this step only!) is designed to be run on the **submit** machine, not **sub-1** at WIPAC. That is, you want to do this with access to the local filesystem, not on the grid.

## Logistical Details
### Setting up the software
These jobs are designed to run on "the grid." They therefore need software that is installed in cvmfs. This is currently being handled by code distributed in [user cvmfs for IceCube](https://wiki.icecube.wisc.edu/index.php/User_CVMFS).

Brian is using a conda environment to handle python and proposal. GSL, NuRadioMC, NuRadioReco, and radiotools are installed in cvmfs itself.

### Submitting jobs
Before submitting jobs, it is important to make sure your grid proxy certificates are good

```
grid-proxy-init -hours 72
export X509_USER_PROXY=/tmp/x509up_u$UID
```

### git maintenance
if you are keeping the repo on sub-1, which has an oudated version of git, you will also need to do:

`git remote set-url origin https://clark2668@github.com/clark2668/grid_scripts.git`

or else pushing won't work
