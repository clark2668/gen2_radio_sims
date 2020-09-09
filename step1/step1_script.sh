#!/bin/bash

# first, load variables
step0dir=$1
step1dir=$2
flavor=$3
energy=$4
czmin=$5
czmax=$6
part=$7

# step0dir is where the step0 files ("how to generate the inputs") will go
# step1dir is where the step1 files ("the input files themselves") will go

# the string holding the flavor, energy, and cos(zenith) bin information
meta_info=${flavor}_${energy}eV_${czmin}_${czmax}
pyscript=${meta_info}_${part}.py

# source icecube env for access to cvmfs
# to start, run an ls in the hope of forcing the automount to see the files
# (we'll try the ls trick throughout the script)
ls /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/
ls /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`

# get the input file
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step0dir}/${flavor}/${meta_info}/${pyscript} ./

# clear out the python path
# and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# move the PROPOSAL config file, and make a "tables" directory locally for PROPOSAL to write intermediate files to
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/simulation/support_files/
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/simulation/support_files/config_PROPOSAL.json
cp /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/simulation/support_files/config_PROPOSAL.json .
mkdir tables

# run the python script
python $pyscript

# bring the results back to the data-warehouse
globus-url-copy ./*hdf5 gsiftp://gridftp.icecube.wisc.edu/${step1dir}/${flavor}/${meta_info}/
