#!/bin/bash

# declare -a dets=("baseline_array" "hex_hybrid_only_array" "hex_shallow_array" "hex_shallowheavy_array")
declare -a dets=("baseline_array" "hex_hybrid_only_array")

declare -a flavs=("e" "mu" "tau")

head_dir="/scratch/brianclark/gen2radiosims/trash/step2/"

for det in "${dets[@]}"
do
    echo $det
    for flav in "${flavs[@]}"
    do
        echo $flav
        grep "events processed" $head_dir/$det/$flav/err/* >> times_${det}_${flav}.txt
        grep "fraction of triggered" $head_dir/$det/$flav/err/* >> triggers_${det}_${flav}.txt
    done
done