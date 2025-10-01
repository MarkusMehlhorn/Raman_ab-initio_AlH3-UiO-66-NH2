#!/bin/bash

for j in {1..6}; do
	cd $j
	echo "$j" 
	grep "HURRAY" orca.out
	grep "imaginary mode" orca.out		
	cd ..
done
