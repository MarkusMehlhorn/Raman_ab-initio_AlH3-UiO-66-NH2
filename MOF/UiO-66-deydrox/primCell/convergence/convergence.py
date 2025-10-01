
import os
import numpy as np
from ase.units import Ry, eV
from pwtools import crys, io
from matplotlib import pyplot as plt
import pandas as pd




def parse_conv(conv):
    print(os.getcwd())
    parameters = [ f.name for f in os.scandir(conv) if f.is_dir() ]
    parameters.remove('template')
    parameters.remove('.idea')
    
    parameterrange=[]
    
    for parameter in parameters:
        parameterrange.append(int(parameter))
    
    parameterrange.sort()
    
    E=[]
    
    for parameter in parameterrange:
        print(parameter)
        structure=io.read_pw_scf(conv+'/'+str(parameter)+'/pw.out')
        E.append(structure.get_etot())
    
    DeltaE=[]
    
    for i in range(len(parameterrange)):
        if i==0:
            DeltaE.append(-1)
        else:
            DeltaE.append(E[i]-E[i-1])
    
    DeltaE_meVperat = 1e3*np.array(DeltaE)/108
    
    print(parameterrange)
    
    lgDeltaE_meVperat=np.log10(-1*DeltaE_meVperat)
    
    data = pd.DataFrame({"parameter": parameterrange, 
                        "Delta E": DeltaE, 
                        "Delta E per at": DeltaE_meVperat, 
                        "lgDeltaE_per_at": lgDeltaE_meVperat})
    
    path='/home/mehlhorn/mnt/TUBAF_home_drive/_Diplomarbeit/Ergebnisse/Daten/'
    
    file=conv+'.csv'
    
    data.to_csv(path+file)
    
    return data

if __name__ == "__main__":
    
    
    for f in os.scandir():
        if f.is_dir():
            parse_conv(f.name)
    
    

        