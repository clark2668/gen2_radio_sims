#!/bin/bash

# first, load variables
step1dir=$1
step2dir=$2
det_file=$3
config_file=$4
sim_file=$5
flavor=$6
energy=$7
czmin=$8
czmax=$9
part=${10}


# step1dir is where the step1 files ("the input files themselves") will go
# step2dir is where the step2 files ("actual simulation output") will go

# the string holding the flavor, energy, and cos(zenith) bin information
meta_info=${flavor}_${energy}eV_${czmin}_${czmax}
inputfile=${meta_info}.part${part}.hdf5
outputfile=out_${meta_info}.part${part}.hdf5

# just so we can have access to gridftp
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`

# get the input file
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step1dir}/${flavor}/${meta_info}/${inputfile} ./

# copy in the relevant detector, config, and simulation files
base_support_dir=/data/user/brianclark/Gen2/simulation_input/support_files
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/${det_file}.json ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/${config_file}.yaml ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/${sim_file}.py ./

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# run the python script
python ${sim_file}.py ${inputfile} ${det_file}.json ${config_file}.yaml ${outputfile}

# bring the results back to the data-warehouse
outdir=${step2dir}/${det_file}/${config_file}/${sim_file}/${flavor}/${meta_info}
globus-url-copy ./out_*hdf5 gsiftp://gridftp.icecube.wisc.edu/${step2dir}/${outdir}/
