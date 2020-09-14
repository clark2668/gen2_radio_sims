# Gen2 Radio Simulations
repository for gen2 radio sims stuff

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

## Simulation Tools and Steps

### pytools
There is a small "helper" class in the `pytools` directory. This standardizes things like the zenith binning, energy binning, etc. To use it, you will need to do:

`export PYTHONPATH=/path/to/pytools:$PYTHONPATH`

### step 0
Step 0 is where we output the "control" files for NuRadioMC that tell NuRadioMC how to distribute the neutrinos that will become the step 1 files. This includes the neutrino energy, zeniths, vertex volume, etc. Run this by doing:

`python make_step0_files.py`

The main parameter, which sits near the top of the file, is the `base_dir`, which is where you ant the step 0 and step 1 files to be placed.

### step 1

### step 2

### step3

## Logistical Details
These jobs are designed to run on "the grid." They therefore need software that is installed in cvmfs.

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
