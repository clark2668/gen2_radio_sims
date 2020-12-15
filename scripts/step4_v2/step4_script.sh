#!/bin/bash

# first, load variables
topdir=$1
flavor=$2
energy=$3
czmin=$4
czmax=$5

# for debugging
# working_dir=$6
# export starting=$PWD

# in production
working_dir=$TMPDIR

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# change something really quickly--important not to do this generally, only do this if you know
# you will try and write to the file with only one core at a time!
export HDF5_USE_FILE_LOCKING='FALSE'

cp -r ${topdir}/${flavor}/${flavor}_${energy}eV_${czmin}_${czmax} $working_dir
cd $working_dir/${flavor}_${energy}eV_${czmin}_${czmax}

# untar the .tar.gz files
for f in *.tar.gz
do
	tar -zxvf $f
done

# run the python script
pyscript=/cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/simulation/NuRadioMC/NuRadioMC/utilities/merge_hdf5.py
python $pyscript ${flavor}_${energy}eV_${czmin}_${czmax}.hdf5 *.hdf5

# send the merged file back to the source location
cp ${flavor}_${energy}eV_${czmin}_${czmax}.hdf5 ${topdir}/${flavor}/.


cd $starting


