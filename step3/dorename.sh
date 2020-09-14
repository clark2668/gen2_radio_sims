#!/bin/bash

# declare -a flavors=("e" "mu" "tau")
declare -a flavors=("e")

top_dir=/data/user/brianclark/Gen2/simulation_output/secondaries_500km2/dipoles_100m/config_Alv2009_nonoise_100ns/D02single_dipole

for flavor in "${flavors[@]}"
do
	for dir in $top_dir/$flavor/*
	do
		echo $dir
		cd $dir
		for f in *.hdf5
		do
			echo "on f "$f
			filename="${f%.*}"
			part="${filename##*.}"
			before_part="${filename%.*}"
			mv $f $before_part.hdf5.$part
		done
		cd ..
	done
done


