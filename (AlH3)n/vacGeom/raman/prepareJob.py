import os
import shutil

def prepareCalc():

    calcs=[1,2,3,4,5,6,7,8]

    for b in calcs:
        a=str(b)
        os.mkdir(a)

        # only confs with less then 3 kcal difference


        with open('template/run.inp', 'r') as f:
            inp_template = f.read()

        with open('template/orca.job', 'r') as f:
            job_template = f.read()

        print(job_template)
        print(inp_template)

        # write job and run files

        shutil.copy('../PBE-TZVP/'+a+'/run.xyz', a+'/start.xyz')

        job = job_template.replace('MMM', 'raman'+a)
        with open(a+'/orca.job', 'w') as f:
            f.write(job)
        with open(a+'/run.inp', 'w') as f:
            f.write(inp_template)


if __name__ == "__main__":

    prepareCalc()
