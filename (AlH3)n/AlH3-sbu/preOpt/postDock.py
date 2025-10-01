
import os
from ase import io

def firstOpt()
    for b in [4,5,6,7,8]:
        a=str(b)+'/'
        os.mkdir(a)
        # read the structures of the final ensemble
        confs = io.read('../docking/'+a+'run.docker.struc1.all.optimized.xyz', index=":")
        
        # only confs with less then 3 kcal difference
        
        print(confs)
        
        with open('template/run.inp', 'r') as f:
            inp_template = f.read()
        
        with open('template/orca.job', 'r') as f:
            job_template = f.read()
        
        print(job_template)
        print(inp_template)
        
        # write job and run files
        for i in range(len(confs)):
            n = str(i)+'/'
            os.mkdir(a+n)
            io.write(a+n+'start.xyz', confs[i], 'xyz')
            job = job_template.replace('MMM', a+"-"+n)
            with open(a+n+'orca.job', 'w') as f:
                f.write(job)
            with open(a+n+'run.inp', 'w') as f:
                f.write(inp_template)

def nextOpt():
    for b in [1,2,3,4,5,6,7,8]:
        a=str(b)
        os.mkdir(a)
        # read the structures of the final ensemble
        confs = io.read('../docking/'+a+'run.docker.struc1.all.optimized.xyz', index=":")
        
        # only confs with less then 3 kcal difference
        
        print(confs)
        
        with open('template/run.inp', 'r') as f:
            inp_template = f.read()
        
        with open('template/orca.job', 'r') as f:
            job_template = f.read()
        
        print(job_template)
        print(inp_template)
        
        # write job and run files
        for i in range(len(confs)):
            n = str(i)+'/'
            os.mkdir(a+n)
            io.write(a+n+'start.xyz', confs[i], 'xyz')
            job = job_template.replace('MMM', a+"-"+n)
            with open(a+n+'orca.job', 'w') as f:
                f.write(job)
            with open(a+n+'run.inp', 'w') as f:
                f.write(inp_template)

if __name__ == "__main__":
    nextOpt()