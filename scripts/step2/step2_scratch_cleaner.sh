#!/bin/bash

declare -a dets=("dipoles_RNOG_100m_2.00km" "dipoles_RNOG_100m_3.00km" "dipoles_RNOG_200m_2.00km" "dipoles_RNOG_200m_3.00km" "surface_4LPDA_1dipole_RNOG_1.00km" "surface_4LPDA_1dipole_RNOG_1.50km")

declare -a flavs=("e" "mu" "tau")

declare -a dirs=("err" "out")

head_dir="/scratch/brianclark/gen2radiosims/trash/"
for det in "${dets[@]}"
do
	for flav in "${flavs[@]}"
	do
		for dir in "${dirs[@]}"
		do
			files=($head_dir/$det/$flav/$dir/*)
			if [ ${#files[@]} -gt 1 ]; then
				for file in "${files[@]}"
				do
					rm $file
				done
			fi			
		done
	done
done