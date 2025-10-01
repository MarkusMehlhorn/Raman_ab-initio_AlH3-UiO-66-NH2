#!/bin/bash

for i in {1..8}; do
	cd $i
	sbatch orca.job
	cd ..
done
