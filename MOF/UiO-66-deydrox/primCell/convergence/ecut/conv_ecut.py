import os
import numpy as np

#defining tested energy cutoffs
ecutrange=np.linspace(60,150,10)
print(ecutrange)

#go to the template directory and read the job and run files
os.chdir('template')
with open('qe.job', 'r') as j:
    jobtemplate=j.read()
with open('pw.inp', 'r') as r:
    runtemplate=r.read()
os.chdir('..')
for ecut in ecutrange:
    os.mkdir(str(ecut))
    os.chdir(str(ecut))
    with open('qe.job', 'w') as j:
        j.write(jobtemplate)
    runtemplate_ecut=runtemplate.replace('MecutM', str(ecut))
    runtemplate_ecut=runtemplate_ecut.replace('MecutrhoM', str(6*ecut))
    with open('pw.inp', 'w') as r:
        r.write(runtemplate_ecut)
    os.system('sbatch qe.job')
    os.chdir('..')