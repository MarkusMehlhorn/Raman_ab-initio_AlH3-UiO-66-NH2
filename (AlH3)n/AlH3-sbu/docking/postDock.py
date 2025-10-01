
import os
from ase import io

base_dir = os.getcwd()
print(base_dir)

# read the structures of the final ensemble
confs = io.read('./calc/run.docker.struc1.all.optimized.xyz', index=":")

# only confs with less then 3 kcal difference

print(confs)

with open('./postDock/template/run_loose.inp', 'r') as f:
    inp_losse_template = f.read()

with open('./postDock/template/run_tight.inp', 'r') as f:
    inp_tight_template = f.read()

with open('./postDock/template/orca.job', 'r') as f:
    job_template = f.read()

print(job_template)
    

# write job and run files
for i in range(11,15):
    n = str(i)
    os.mkdir('./postDock/'+n)
    io.write('./postDock/'+n+'/start.xyz', confs[i], 'xyz')
    job = job_template.replace('MMM', n)
    with open('./postDock/'+n+'/orca.job', 'w') as f:
        f.write(job)
    with open('./postDock/'+n+'/run_loose.inp', 'w') as f:
        f.write(inp_losse_template)
    with open('./postDock/'+n+'/run_tight.inp', 'w') as f:
        f.write(inp_tight_template)

for i in range(11,15):
    os.chdir('./postDock/'+str(i))
    os.system('sbatch orca.job')
    os.chdir(base_dir)
