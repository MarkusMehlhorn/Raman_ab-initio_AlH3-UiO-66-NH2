import os

#defining tested energy cutoffs
ecutrho_multiplyer=6
ecut=150 #Ry

Ns=list(range(1,4))
Ns.reverse()

#go to the template directory and read the job and run files
os.chdir('template')
with open('qe.job', 'r') as j:
    jobtemplate=j.read()
with open('pw.inp', 'r') as r:
    runtemplate=r.read()
os.chdir('..')
for N in Ns:
    os.mkdir(str(N))
    os.chdir(str(N))
    with open('qe.job', 'w') as j:
        j.write(jobtemplate)
    runtemplate_ecut=runtemplate.replace('MecutM', str(ecut))
    runtemplate_ecutrho=runtemplate_ecut.replace('MecutrhoM', str(ecutrho_multiplyer*ecut))
    runtemplate_N=runtemplate_ecutrho.replace('MMM', str(N))
    with open('pw.inp', 'w') as r:
        r.write(runtemplate_N)
    os.system('sbatch qe.job')
    os.chdir('..')
