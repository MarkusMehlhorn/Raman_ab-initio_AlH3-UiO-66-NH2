
import os
import shutil
import io
import pandas as pd
import numpy as np


from matplotlib import pyplot as plt

import ase.io
from ase.units import kJ, Ha, mol, kcal




associates = [1,2,3,4,5,6,7,8]

def readDock():
    dataDock=[]
    for associate in associates:
        print("read"+str(associate), end=' ')
        dataDock.append(pd.read_csv('../../AlH3-sbu/preOpt/tabels/'+str(associate)+'.csv'))
    print()
    return dataDock

def parseOrcaDocker(file):
    with open(file,'r') as f:
        fl = f.readlines()
        for i,l in enumerate(fl):
            if "Running final optimization" in l:
                init = i
            elif "Maximum number of structures" in l:
                n = int(l.split(" ")[-1])
                print()
        table = ""
        i=init+10+4
        while True:
            table = table + fl[i]
            i=i+1
            if fl[i].strip()=="" and i > init+10+4:
                break
        return table


def parseDock():      
    
    data=[]
    
    host = ase.io.read('../../MOF/UiO-66-deydrox/sbu/GeomOpt/SVP-gCp/orca.out', index=-1, format="orca-output")
    Ehost = host.get_total_energy()/kcal*mol
    print("Ehost", Ehost)
    
    for associate in associates:
        a = str(associate)
        print("-----------------------\n Parse Docking "+a+"\n-----------------------\n")
        dataDockStr = io.StringIO(parseOrcaDocker('docking/'+a+"/orca.out"))
        dataDockNp = np.transpose(np.loadtxt(dataDockStr))
        dataDock = pd.DataFrame({"ind": dataDockNp[0], "E(FF)": dataDockNp[1], "E_ia(FF)": dataDockNp[2]})       
        
        
        cluster = ase.io.read('../vacGeom/PBE-SVP-gCp/'+a+'/orca.out', index=-1, format="orca-output")
        Ecluster = cluster.get_total_energy()/kcal*mol
        print("Ecluster", Ecluster)
        Esep = Ecluster + Ehost
        print("Esep", Esep) 
        
        n_conf = len(dataDock["ind"])
        etot=[]
        print("reading preOpt structures")
        for i in range(n_conf):
            ind = str(i)
            print(i,end=" ")
            atoms = ase.io.read('preOpt/'+a+'/'+ind+'/orca.out', index=-1, format='orca-output')
            etot.append(atoms.get_total_energy()/kcal*mol - Esep)
            
        print()    
        dataDock["E_ia(PBE)"] = etot
        dataDock = dataDock.sort_values(by="E_ia(FF)")
        dataDock["Sort(FF)"]=list(range(1, n_conf+1))
        
        
        
        dataDock = dataDock.sort_values(by="E_ia(PBE)")
        dataDock["Sort(PBE)"]=list(range(1, n_conf+1))
        
        print("preOpt "+a+"\n")
        print(dataDock)
        data.append(dataDock)
        dataDock.to_csv('preOpt/tabels/'+a+'.csv')
        
        plt.figure(1)
        plt.scatter(dataDock["Sort(FF)"], dataDock["E_ia(FF)"])
        plt.title("Docking "+a)
        plt.ylabel("interaction energy [kcal/mol]")
        plt.savefig('plots/dock'+a+'.png', dpi=400)
        plt.show()
        plt.close(1)
        
        plt.figure(1)
        plt.scatter(dataDock["Sort(PBE)"], dataDock["E_ia(PBE)"])
        plt.title("DockingOpt "+a)
        plt.ylabel("interaction energy [kcal/mol]")
        plt.savefig('plots/dockOpt'+a+'.png', dpi=400)
        plt.show()
        plt.close(1)
        
        
        
    return data

def prepareMinStruct(dataDock):
    
    print('prepare MinStructures')
    
    with open('template/run_pre.inp', 'r') as f:
        inp_pre_template = f.read()
    
    with open('template/run.inp', 'r') as f:
        inp_template = f.read()
    
    with open('template/orca.job', 'r') as f:
        job_template = f.read()
    
    for i, associate in zip(associates,dataDock):
        print(associate)
        minimum = int(associate.loc[associate["Sort(PBE)"] == 1, "ind"].values[0])-1
        print(minimum, end=' ')
        print()
        
        
        job = job_template.replace("MMM", str(i))
        shutil.copy('../../AlH3-sbu/preOpt/'+str(i)+'/'+str(minimum)+'/run.xyz', str(i)+'/start.xyz')
        with open(str(i)+'/orca.job', 'w') as f:
            f.write(job)
        with open(str(i)+'/run.inp', 'w') as f:
            f.write(inp_template)
        with open(str(i)+'/run_pre.inp', 'w') as f:
            f.write(inp_pre_template)


if __name__ == "__main__":   
    

    dataDock=readDock()

    
    prepareMinStruct(dataDock)
        

    
    
        
        
        
    
    
    
        