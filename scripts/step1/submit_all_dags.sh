#!/bin/bash

FILES=dagman_step1_*.dag
for f in $FILES
do
	condor_submit_dag $f
done
