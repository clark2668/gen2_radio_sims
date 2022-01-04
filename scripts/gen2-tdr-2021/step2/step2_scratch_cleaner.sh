#!/bin/bash

declare -a dets=("baseline_array" "hex_hybrid_only_array" "hex_shallow_array" "hex_shallowheavy_array")

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