#!/bin/bash
#
#
for i in {1..8}; do
	cd $i
	orca_mapspc orca.out raman -w20 -x00 -x13000 -oraman.dat
	cd ..
done
