#!/bin/bash

for j in {4..8}; do
	cd $j
	for i in $(find . -maxdepth 1 -type d ! -name '.'); do
		cd $i
		sbatch orca.job
		cd ..
	done
	cd ..
done
