#!/bin/bash

for i in {1..8}; do
	mkdir $i
	cp ../raman/$i/run.xyz $i/start.xyz
	cp template/* $i
	sed -i "s/MMM/$i/g" $i/orca.job
done
