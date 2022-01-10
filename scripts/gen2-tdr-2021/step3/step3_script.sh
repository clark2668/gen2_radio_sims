#!/bin/bash

# first, load variables
step3dir=$1
step2dir=$2
flavor=$3
energy=$4
czmin=$5
czmax=$6

echo "czmin is "$czmin

# for debugging
# working_dir=$6
export starting=$PWD

# in production
working_dir=$TMPDIR

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

# change something really quickly--important not to do this generally, only do this if you know
# you will try and write to the file with only one core at a time!
export HDF5_USE_FILE_LOCKING='FALSE'

cp -r ${step2dir}/${flavor}/${flavor}_${energy}eV_${czmin}_${czmax} $working_dir
cd $working_dir/${flavor}_${energy}eV_${czmin}_${czmax}
ls

pyscript=/home/brianclark/Gen2/radio/gen2_radio_sims/scripts/gen2-tdr-2021/step3/merge_hdf5.py

# run directly on the .tar.gz files now
outfile=${flavor}_${energy}eV_${czmin}_${czmax}.hdf5
python $pyscript $outfile *.hdf5.tar.gz

if test -f "$outfile"; then

    echo "$outfile HDF5 exists -- continue with tarring and transferring"

    # send the merged file back to the source location
    cp ${outfile} ${step3dir}/${flavor}/.

else
    echo "$outfile HDF5 does NOT exist -- simulation failed for some reason"
    exit 1
fi

cd $starting


