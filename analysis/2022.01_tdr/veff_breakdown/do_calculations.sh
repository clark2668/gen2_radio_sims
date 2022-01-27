declare -a dets=("0" "1" "2" "3")
# declare -a dets=("0" "2")

declare -a modes=("deepshallow" "hybridshallow")

for det in "${dets[@]}"
do
    for mode in "${modes[@]}"
    do
        python calc_fractions.py --det $det --mode $mode # first, calculate the information
        python plot_veffs.py --det $det --mode $mode # now, make plots and write to csv
    done
done

declare -a modes=("advanced")

for det in "${dets[@]}"
do
    for mode in "${modes[@]}"
    do
        python calc_fractions_advanced.py --det $det --mode $mode # first, calculate the information
        python plot_veffs_advanced.py --det $det --mode $mode # now, make plots and write to csv
    done
done
