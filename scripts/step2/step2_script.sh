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
inputfile=in_${meta_info}.part${part}.hdf5
inputtarfile=${inputfile}.tar.gz
outputfile=${meta_info}.part${part}.hdf5

# just so we can have access to gridftp
ls /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`

# get the input file
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step1dir}/${flavor}/${meta_info}/${inputtarfile} ./
tar -xvzf ${inputtarfile}

# copy in the relevant detector, config, and simulation files
base_support_dir=/data/sim/Gen2/radio/2020/simulation_input/support_files/analysis-scripts/gen2-design-2020
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/detector/${det_file}.json ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/config/${config_file}.yaml ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/detsim/${sim_file}.py ./

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# run the python script
python ${sim_file}.py ${inputfile} ${det_file}.json ${config_file}.yaml ${outputfile}

# cleanup the input hdf5 file
rm in_*.hdf5

# bring the results back to the data-warehouse
outdir=${step2dir}/${det_file}/${config_file}/${sim_file}/${flavor}/${meta_info}
globus-url-copy ./*hdf5 gsiftp://gridftp.icecube.wisc.edu/${outdir}/
