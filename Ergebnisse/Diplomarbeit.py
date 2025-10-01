import sys
import os
import json

import plots
import postProcessing
import tables
sys.path.append('/home/mehlhorn/mnt/noether/Skripte/')
from ComChemTools import parse
from ComChemTools import pathfinder





def convTest():
    plots.convTest()

def basisset():
    parse.basisSets()
    postProcessing.basisset()
    
def clusterEnergies():
    parse.all_Energies()
    postProcessing.solvintEnergies()
    plots.ClusterEnergies()
    tables.percentE()

def raman_spectra():
    parse.ramanSpectra()
    plots.raman_spectra()

def raman_modes():
    parse.raman_modes()
    postProcessing.raman_modes(50)
  

if __name__ == "__main__":
    
    clusterEnergies()
    
    print('done Diplomarbeit')