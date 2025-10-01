#!/bin/bash
#
#
for i in PBE0-DH PBE0 PBE PBEh-3c r2SCAN-3c; do
	cd $i
	orca_mapspc orca.out raman -w20 -x00 -x12200 -oraman.dat
        cd ..
done
