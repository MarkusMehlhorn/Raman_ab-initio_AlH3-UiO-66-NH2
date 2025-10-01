
from config import * 

import pickle
import json

import pandas as pd
from ase.units import Ha, kJ, mol, Ry
from sklearn.metrics import root_mean_squared_error as rmsd
import numpy as np

Daten_path='/home/mehlhorn/mnt/TUBAF_home_drive/_Diplomarbeit/Ergebnisse/Daten/'



def processAll():
    raman_modes(50, 50)
    impregnationEnergy()
    solvintEnergies()

def basisSets():

    data=pd.read_csv(Daten_path+'basissetE.csv')
     
    data["$\Delta E_\\text{el}$"]=data["total energy"]-data["total energy"][6]
    
    
    print(data)
    
    data.to_csv(Daten_path+'basissetE.csv')
    

def docking():
    with open(Daten_path+'rawDocking.pkl', 'rb') as f:
        rawdata = pickle.load(f)
    
    with open(Daten_path+'referenceDocking.pkl', 'rb') as f:
        references = pickle.load(f)
    
    
    print("reference:")
    print(references)    
    
    cov_PBE_GFN = pd.DataFrame({"n": [c for c in range(1,9)]})
    cov = []
    
    for frame, reference, cluster in zip(rawdata, references, [i for i in range(1,9)]):
        print()
        print(cluster)
        data = frame
        data["\DE{int}{el,PBE}"] = data["$E_\text{el,PBE}$"] - reference
        cov.append(np.corrcoef(np.array([data["\DE{int}{el,PBE}"], data["\DE{int}{el,GFN_FF}"]]))[0, 1])
        if cluster==7:
            print('hit')
            print(data[data["conf. Nr"]==15].index)
            i=data[data["conf. Nr"]==15].index
            data = data.drop(14)
            
        print(data)
        print("saving data")
        data.to_csv(Daten_path+"docking/"+str(cluster)+".csv")
        
    cov_PBE_GFN["corr(PBE,GFN-FF)"] = cov
        
        
    print("saving correlation")
    cov_PBE_GFN.to_csv(Daten_path+"docking/corr.csv")
    print()
    

def raman_modes(ramanThreshold, matchThreshold):
    print("reading raw Raman")
    with open(Daten_path+'raman/rawData.pkl', 'rb') as f:
        rawdata = pickle.load(f)
    
    print("filtering by Raman activity")
    data = {}
    data = raman_filter(rawdata, data, [models[0], models[1]], ramanThreshold)
    data = raman_filter(rawdata, data, [models[2], models[3]], ramanThreshold)
       
    # get rmsd 
    clusterRMSD =[]
    clust = []
    for clusterSize in [str(c) for c in clusterSizes]:
        clusterRMSD.append(rmsd(data[models[1]][clusterSize], 
                                data[models[0]][clusterSize]))
        clust.append(clusterSize)
    
    clusters = pd.DataFrame({'Cluster':clust, 'rmsd':clusterRMSD})
    print(clusters)
    
    print("matching cluster and sbu+cluster modes")
    for clusterSize in [str(c) for c in clusterSizes]:
        data[models[2]][clusterSize] = sbu_raman_matcher(data[models[2]][clusterSize], 
                                                     data[models[0]][clusterSize], 
                                                     matchThreshold)
    
    return data


    
    
    
def raman_filter(rawdata, data, models, threshold):
    # filter modes by raman activity
    for model in models:
        data[model] = {}
        for clusterSize in rawdata[model]:
            data[model][clusterSize] = rawdata[model][clusterSize][(rawdata[models[0]][clusterSize]["activity"]>threshold) & 
                                                                   (rawdata[models[1]][clusterSize]["activity"]>threshold)]
    return data
    
    
        
def sbu_raman_matcher(df1, df2, threshold):
    
    # Function to filter df1 rows within threshold of df2 frequencies
    mask = df1['frequency'].apply(
        lambda f1: any(abs(f1 - f2) <= threshold for f2 in df2['frequency'])
    )
    
    filtered_df1 = df1[mask]
    
    return filtered_df1
    

def impregnationEnergy():
    """
    calculate assoiation energies
    """
    
    with open(Daten_path+'refSysEnergies.json', 'r') as f:
        ref = json.load(f)
    path=Daten_path+'/rawEnergies.csv'
    rawE = pd.read_csv(path)
    
    impEelm = pd.DataFrame({'n':[n for n in range(1,9)], models[0]:None, models[1]:None})
    print(rawE)

    # normalization and substraction of alpha-AlH3
    
    alpha = -2935.003147/6 *Ry /kJ*mol# ref['alpha-AlH3']/6 *Ry
    AlH3 = rawE[models[0]][rawE['n']==1][0]

    impEelm[models[0]] = (rawE[models[0]]  /rawE['n'] -AlH3)*Ha/kJ*mol
    impEelm[models[1]] = (rawE[models[1]]  /rawE['n'] - AlH3)*Ha/kJ*mol
    impEelm[models[2]] = ((rawE[models[2]] - (rawE['n']*AlH3 +ref['sbu'] ))/rawE['n'])*Ha/kJ*mol
    impEelm[models[3]] = ((rawE[models[3]] - (rawE['n']*AlH3 +ref['sbu+solv'] ))/rawE['n'])*Ha/kJ*mol
    
    print(rawE['n']*AlH3 +ref['sbu+solv'])
    
    print(ref)
    print(impEelm)
    
    impEelm.to_csv(Daten_path+'/asEelm.csv')    

def solvintEnergies():
    print("reading energies")
    energies = pd.read_csv(Daten_path+'/asEelm.csv')
    delta = pd.DataFrame({'n':[n for n in range(1,9)]})
    
    delta[models[1]] = energies[models[1]] - energies[models[0]]
    delta['int'] = energies[models[2]] - energies[models[0]]
    delta['imp'] = energies[models[3]] - energies[models[0]]
    delta['solv,int'] = delta['imp'] -delta[models[1]] -delta['int']
    
    print(delta)
    
    print("writing energy differences")
    delta.to_csv(data_path+'/deltaE.csv')
    
    print("calculating relative contributions")
    share = pd.DataFrame()
    for contribution in delta.keys():
        if contribution == 'n' :
            share[contribution] = delta[contribution]
        else:
            share[contribution] = delta[contribution]/delta['imp']*100
    print(share)
    
    print("writing relative contributions")
    share.to_csv(data_path+'/percentE.csv')

if __name__ == "__main__":
    
    basisSets()
    
    print('postProcessing check') 
    
    