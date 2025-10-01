#!/bin/bash
#
#
DIRS=$(find . -mindepth 1 -maxdepth 1 -type d)

for dir in $DIRS;
do
	echo $dir
	mkdir $dir/start
	mkdir $dir/calc
done
