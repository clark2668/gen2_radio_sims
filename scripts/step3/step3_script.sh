#!/bin/bash

# first, load variables
step2dir=$1
step3dir=$2
step2detfile=$3
det_file=$4
config_file=$5
sim_file=$6
flavor=$7
energy=$8
czmin=$9
czmax=${10}
part=${11}


# step2dir is where the step2 input files are (the "pass1" files)
# step3dir is where the step3 output files are (the "pass2" files)

# the string holding the flavor, energy, and cos(zenith) bin information
meta_info=${flavor}_${energy}eV_${czmin}_${czmax}
inputfile=${meta_info}.part${part}.hdf5
altinputfile=${meta_info}.hdf5.part${part}
outputfile=pass2_${meta_info}.part${part}.hdf5

# just so we can have access to gridftp
ls /cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.1.1/setup.sh`

# get the input file (bit naughty to hard code the step 2 config and detsim file, but oh well...)
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step2dir}/${step2detfile}/config_Alv2009_nonoise_100ns/D02single_dipole_250MHz/${flavor}/${meta_info}/${inputfile} ./
if [ $? -ne 0 ]; then
	echo "$inputfile file copy failed... try again with hdf5.part version..."
	rm ${inputfile} # we have to remove this because apparently globus-url-copy can leave ghost files...
	inputfile=${altinputfile}
	globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${step2dir}/${step2detfile}/config_Alv2009_nonoise_100ns/D02single_dipole_250MHz/${flavor}/${meta_info}/${inputfile} ./
	if [ $? -ne 0 ]; then
		echo "$inputfile copy failed ... abort completely."
		rm ${inputfile} # we have to remove this because apparently globus-url-copy can leave ghost files...
		exit 1
	fi
fi

# copy in the relevant detector, config, and simulation files
base_support_dir=/data/sim/Gen2/radio/2020/simulation_input/support_files/analysis-scripts/gen2-design-2020
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/detector/${det_file}.json ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/config/${config_file}.yaml ./
globus-url-copy gsiftp://gridftp.icecube.wisc.edu/${base_support_dir}/detsim/${sim_file}.py ./

# clear out the python path and source the setup file for gen2 radio simulations
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

if [ -f $inputfile ]; then
	echo "$inputfile exists - proceed with simulation"

	# run the python script
	python ${sim_file}.py ${inputfile} ${det_file}.json ${config_file}.yaml ${outputfile}

	# cleanup the input hdf5 file
	rm ${inputfile}

	if [ -f $outputfile ]; then
		echo "$outputfile exists -- simulation at least produced output"

		# tar up the result
		tar -czvf ${outputfile}.tar.gz ${outputfile}

		# bring the results back to the data-warehouse
		outdir=${step3dir}/${det_file}/${config_file}/${sim_file}/${flavor}/${meta_info}
		globus-url-copy ./*gz gsiftp://gridftp.icecube.wisc.edu/${outdir}/

		exit 0
	else
		echo "$outputfile does NOT exist -- simulation failed for some reason"
		exit 1
	fi
fi


