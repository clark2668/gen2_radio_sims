#!/bin/bash

# load variables
step3dir=$1
step4dir=$2
detfile=$3
configfile=$4
simfile=$5
flavor=$6

# for debugging
# working_dir=$6
export starting=$PWD

# in production
working_dir=$TMPDIR

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

export HDF5_USE_FILE_LOCKING='FALSE'
cp /home/brianclark/Gen2/radio/gen2_radio_sims/scripts/gen2-tdr-2021/step4/Veff.py .
cp /home/brianclark/Gen2/radio/gen2_radio_sims/scripts/gen2-tdr-2021/step4/step4.py .
python step4.py ${step3dir}/${detfile}/${configfile}/${simfile}/${flavor} ${flavor} ${detfile} ${configfile} ${simfile}

# send the merged file back to the source location
mv *.pkl ${step4dir}/.

cd $starting
