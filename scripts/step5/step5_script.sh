#!/bin/bash

# load variables
step4dir=$1
step5dir=$2
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


## old version, where we copy all the files, but that's inefficient, because the inputs can be really large...
#####
#####
#####
#cp -r ${step4dir}/${detfile}/${configfile}/${simfile}/${flavor} $working_dir
#cd $working_dir

## run the python script
#pyscript=/home/brianclark/Gen2/gen2_radio_sims/scripts/step5/step5.py
#python $pyscript ${flavor} ${flavor} ${detfile} ${configfile} ${simfile}
## no, that's (^) not a mistake. the flavor is also the name of the path to the directory in this case
#####
#####
#####

export HDF5_USE_FILE_LOCKING='FALSE'

## v2, run on files in place, use Veff.py in cvmfs
#####
#####
#####
# pyscript=/home/brianclark/Gen2/gen2_radio_sims/scripts/step5/step5.py
# python $pyscript ${step4dir}/${detfile}/${configfile}/${simfile}/${flavor} ${flavor} ${detfile} ${configfile} ${simfile}

## v3, run on files in place, use Veff.py in step5 folder (cuz I'm impatient with cvmfs)
#####
#####
#####
cp /home/brianclark/Gen2/gen2_radio_sims/scripts/step5/Veff.py .
cp /home/brianclark/Gen2/gen2_radio_sims/scripts/step5/step5.py .
python step5.py ${step4dir}/${detfile}/${configfile}/${simfile}/${flavor} ${flavor} ${detfile} ${configfile} ${simfile}


# send the merged file back to the source location
mv *.pkl ${step5dir}/.

cd $starting
