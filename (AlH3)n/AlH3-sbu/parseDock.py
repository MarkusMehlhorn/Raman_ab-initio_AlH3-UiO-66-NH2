
import os
import io
import pandas as pd
import numpy as np


from matplotlib import pyplot as plt

import ase.io
from ase.units import kJ, Ha, mol, kcal




associates = [1,2,3,4,5,6,7,8]



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

    host = ase.io.read('../../MOF/UiO-66-deydrox/sbu/GeomOpt/SVP-gCp/orca.out', index=-1, format="orca-output")
    Ehost = host.get_total_energy()/kcal*mol
    print("Ehost", Ehost)
    
    for associate in associates:
        a = str(associate)
        print("-----------------------\n Parse Docking "+a+"\n-----------------------\n")
        dataDockStr = io.StringIO(parseOrcaDocker('docking/'+a+"/orca.out"))
        dataDockNp = np.transpose(np.loadtxt(dataDockStr))
        dataDock = pd.DataFrame({"ind": dataDockNp[0], "E": dataDockNp[1], "E_ia": dataDockNp[2]})
        dataDock = dataDock.sort_values(by="E_ia")
        n_conf = len(dataDock["ind"])
        dataDock["Sort"]=list(range(1, n_conf+1))
        print(dataDock)
        
        
        plt.figure(1)
        plt.scatter(dataDock["Sort"], dataDock["E_ia"])
        plt.title("Docking "+a)
        plt.ylabel("interaction energy [kcal/mol]")
        plt.savefig('plots/dock'+a+'.png', dpi=400)
        plt.show()
        plt.close(1)
        
        cluster = ase.io.read('../vacGeom-SVP-gCp/'+a+'/orca.out', index=-1, format="orca-output")
        Ecluster = cluster.get_total_energy()/kcal*mol
        print("Ecluster", Ecluster)
        Esep = Ecluster + Ehost
        print("Esep", Esep) 
    
        etot=[]
        print("reading preOpt structures")
        for i in range(n_conf):
            ind = str(i)
            print(i,end=" ")
            atoms = ase.io.read('preOpt/'+a+'/'+ind+'/orca.out', index=-1, format='orca-output')
            etot.append(atoms.get_total_energy()/kcal*mol - Esep)
        print()    
        n_conf = len(dataDock["ind"])
        dataDockOpt=pd.DataFrame({"ind": list(range(1, n_conf+1)), "E_ia": etot})
        dataDockOpt = dataDockOpt.sort_values(by="E_ia")
        dataDockOpt["Sort"]=list(range(1, n_conf+1))
        print("preOpt "+a+"\n", dataDockOpt)
        
        data.append(dataDockOpt)
        
        plt.figure(1)
        plt.scatter(dataDockOpt["Sort"], dataDockOpt["E_ia"])
        plt.title("DockingOpt "+a)
        plt.ylabel("interaction energy [kcal/mol]")
        plt.savefig('plots/dockOpt'+a+'.png', dpi=400)
        plt.show()
        plt.close(1)
    
    return data
        
if __name__ == "__main__":   
    
    os.chdir('..')
    dataDock = parseDock()
    os.chdir('minStructOpt')
    
   # for i, associate in enumerate(dataDock)
        
    #    minimum = associate["Sort", ind=0]
     #  print(minimum)
    
    
        
        
        
    
    
    
        