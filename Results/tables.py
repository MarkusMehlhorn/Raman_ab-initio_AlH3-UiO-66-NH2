
from config import *

import pandas as pd

def tablesAll():
    rawEnergies()
    deltaE()
    percentE()
    corr()

def OffClipLaTeX():
    epsilon = pd.read_clipboard()
    print(epsilon)
    epsilon.to_latex('../einkleben/Auswertung/mof/epsilon.tab', float_format="%.3f" )

def rawEnergies():
    print("raw Energy table")
    table = pd.read_csv(data_path+'/rawEnergies.csv')
    table.to_latex(dest_path+'AlH3/rawEnergies.tab')

def deltaE():
    print("Energy differences table")
    table = pd.read_csv(data_path+'/deltaE.csv')
    table.to_latex(dest_path+'AlH3/deltaE.tab')

def percentE():
    print("relative Energy contributions table")
    table = pd.read_csv(data_path+'/percentE.csv')
    table.to_latex(dest_path+'AlH3/percentE.tab', columns=['n', 'solv', 'int', 'solv,int'], float_format="%.0f")

def corr():
    print("docking correlation")
    table = pd.read_csv(data_path+'/docking/corr.csv')
    table.to_latex(dest_path+'AlH3/corr.tab')

def basisset():
    print("table basisset")
    table = pd.read_csv(data_path+'/basissetE.csv')
    table.to_latex(dest_path+'/basissetE.tab')

    
if __name__ == "__main__":
    tablesAll()
    print("done tables")
    