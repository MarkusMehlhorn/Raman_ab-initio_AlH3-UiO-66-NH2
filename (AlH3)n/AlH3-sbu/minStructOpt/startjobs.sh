#!/bin/bash

for j in {1..8}; do
	cd $j
	sbatch orca.job
	cd ..
done
