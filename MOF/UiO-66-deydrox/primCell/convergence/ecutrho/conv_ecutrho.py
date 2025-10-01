import os

#defining tested energy cutoffs
ecutrho_multiplyers=list(range(4,12))
ecut=150 #Ry


#go to the template directory and read the job and run files
os.chdir('template')
with open('qe.job', 'r') as j:
    jobtemplate=j.read()
with open('pw.inp', 'r') as r:
    runtemplate=r.read()
os.chdir('..')
for ecutrho_multiplyer in ecutrho_multiplyers:
    print(ecutrho_multiplyer)
    os.mkdir(str(ecutrho_multiplyer))
    os.chdir(str(ecutrho_multiplyer))
    with open('qe.job', 'w') as j:
        j.write(jobtemplate)
    runtemplate_ecutrho=runtemplate.replace('MecutM', str(ecut))
    runtemplate_ecutrho=runtemplate_ecutrho.replace('MecutrhoM', str(ecutrho_multiplyer*ecut))
    with open('pw.inp', 'w') as r:
        r.write(runtemplate_ecutrho)
    os.system('sbatch qe.job')
    os.chdir('..')
