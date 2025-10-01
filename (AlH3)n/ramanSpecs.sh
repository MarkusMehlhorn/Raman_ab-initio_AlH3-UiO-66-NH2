#!/bin/bash
#


for m in "vacGeom" "LöMi" "AlH3-sbu" "AlH3-LöMi-sbu"; do
	cd $m/raman
	echo $cwd
	for i in {1..8}; do
		cd $i
		orca_mapspc orca.out raman -w15 -x00 -x12100 -oraman.dat
		cd ..
	done
	cd ../..
done

