#!/bin/bash

for i in {1..8}; do
	mkdir $i
	cp ../PEGS_Geom/AlH3-$i.xyz $i/start.xyz
	cp template/* $i
	sed -i "s/MMM/$i/g" $i/orca.job
done
