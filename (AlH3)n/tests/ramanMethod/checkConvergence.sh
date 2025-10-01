#!/bin/bash


for i in PBE0-DH PBE PBE0 PBEh-3c r2SCAN-3c; do
	echo $i
	grep "HURRAY" $i/orca.out
	grep "imaginary mode" $i/orca.out
done

