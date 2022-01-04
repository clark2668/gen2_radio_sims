#!/bin/bash

FILES=dagman_step2_*.dag
for f in $FILES
do
	condor_submit_dag $f
done
