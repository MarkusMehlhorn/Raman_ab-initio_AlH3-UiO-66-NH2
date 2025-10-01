#!/bin/bash

for j in {4..8}; do
	cd $j
	for i in $(find . -maxdepth 1 -type d ! -name '.'); do
		cd $i
		echo "$j - $i"^ 
		grep "HURRAY" orca.out
		grep "imaginary mode" orca.out		
		cd ..
	done
	cd ..
done
