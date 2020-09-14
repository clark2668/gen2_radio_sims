# gen2_radio_sims
repository for gen2 radio sims stuff

## simulation strategy

The strategy for the simulation requires two a few main stages:

- step 0: create the configuration files for how to distribute the vertices, zeniths, azimuths, energies, etc of incident neutrinos
- step 1: generate a list of energy depositions in the ice based on the neutrino primaries from step 0 (from neutrino primary interactions, but also secondary interactions like pair production, etc. in the case of electron and muon neutrinos)
- step 2: propagate radio emission from the energy depositions in step 1 to a simulated station
-step 3: combine all of the small "output" files into a single main file

Step 0 and 1 are likely to be reused for many different simulation settings. Step 2 and 3 need to be redone depending on the detector, trigger settings, choice of physics models, etc.

### step 0

### step 1

### step 2

### step3

## bookeeping
These jobs are designed to run on the "grid" in IceCube speak.


### to submit jobs, need to do
grid-proxy-init -hours 72

export X509_USER_PROXY=/tmp/x509up_u$UID

### git maintenance
if you are keeping the repo on sub-1, which has an oudated version of git, you will also need to do:

`git remote set-url origin https://clark2668@github.com/clark2668/grid_scripts.git`

or else pushing won't work
