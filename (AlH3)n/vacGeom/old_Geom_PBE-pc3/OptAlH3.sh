
#!/bin/bash
#
#
DIRS=$(seq 1 8)
echo $DIRS

for dir in $DIRS;
do
        echo $PWD
	sed "s|MMM|${dir}|" <jobrun/orca.job >$dir/start/orca.job 
        cp jobrun/run.inp $dir/start/
	cp $dir/start/* $dir/calc/
	cd $dir/calc/
	sbatch orca.job
	cd ../..
done

