#!/bin/bash

for i in {1..8}; do
	mkdir $i
	cp ../../vacGeom-PBE-pc-1/$i/run.xyz $i/guest.xyz
	cp template/* $i
	sed -i "s/MMM/$i/g" $i/orca.job
done
