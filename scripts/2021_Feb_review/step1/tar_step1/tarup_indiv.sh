#!/bin/bash

declare -a flavors=("tau")

#for flavor in "${flavors[@]}"
#do
#	dirlist=${flavor}_*
#	echo $dirlist
#	for dir in $dirlist
#	do
#		cd $dir
#		files=*.hdf5
#		
#		for file in $files
#		do
#			echo $file
#			tar -czvf ${file}.tar.gz $file
#			rm $file
#		done
#		cd ..
#	done
#done

files=*.hdf5
for file in $files
do
#	echo $file
	tar -czvf ${file}.tar.gz $file
	rm $file
done
