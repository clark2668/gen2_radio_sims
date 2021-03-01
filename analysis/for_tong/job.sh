#!/bin/bash
unset PYTHONPATH
ls /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh
source /cvmfs/icecube.opensciencegrid.org/users/brianclark/gen2radiosim/setup.sh

cp /home/brianclark/Gen2/for_tong/1e18_n1e6_1015_v121.part0000.hdf5 .
cp /home/brianclark/Gen2/for_tong/config.yaml .
cp /home/brianclark/Gen2/for_tong/RNOGv6.json .
cp /home/brianclark/Gen2/for_tong/runThreeStr.py .

python runThreeStr.py 1e18_n1e6_1015_v121.part0000.hdf5 RNOGv6.json config.yaml result.hdf5
cp result.hdf5 /home/brianclark/Gen2/for_tong/.