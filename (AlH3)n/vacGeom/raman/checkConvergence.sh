#!/bin/bash

for j in {1..8}; do
	cd $j
	echo "$j - $i"^
	grep "HURRAY" orca.out
	grep "imaginary mode" orca.out
	grep "ORCA TERMINATED NORMALLY" orca.out
	cd ..
done
