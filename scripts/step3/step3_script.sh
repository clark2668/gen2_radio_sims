#!/bin/bash

# first, load variables
topdir=$1
flavor=$2

# step2dir is where the step2 files ("actual simulation output") will go
# flavor is the flavor 

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# change something really quickly--important not to do this generally, only do this if you know
# you will try and write to the file with only one core at a time!
export HDF5_USE_FILE_LOCKING='FALSE'

# run the python script
pyscript=/cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/simulation/NuRadioMC/NuRadioMC/utilities/merge_hdf5.py
python $pyscript $topdir/$flavor
