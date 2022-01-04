#!/bin/bash

# first, load variables
topdir=$1
flavor=$2
energy=$3
czmin=$4
czmax=$5

# tar up the .hdf5 files to make them take less space

cd ${topdir}/${flavor}/${flavor}_${energy}eV_${czmin}_${czmax}/
files=*.hdf5
for file in $files
do
	tar -czvf ${file}.tar.gz $file
	rm $file
done
