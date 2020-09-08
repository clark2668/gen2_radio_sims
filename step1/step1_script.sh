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
pyscript=${dir}_${part}.py

# just so we can have access to gridftp
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`

# get the input file
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step0dir}/${flavor}/${meta_info}/${pyscript} ./

# clear out the python path
# and source the setup file for gen2 radio simulations
unset PYTHONPATH
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# run the python script
python $pyscript

# bring the results back to the data-warehouse
globus-url-copy ./*hdf5 gsiftp://gridftp.icecube.wisc.edu/${step1dir}/${flavor}/${meta_info}/
