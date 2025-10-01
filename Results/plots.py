


import os
import pickle

import pandas as pd
import matplotlib.pyplot as plt
from ase import io
from ase.units import Hartree # Used for converting eV (ASE's default) to Hartrees

from config import *


# global plot settings
import scienceplots
plt.style.use('science')
plt.rcParams['text.usetex'] = True
colors = ['#007b99', '#b71e3f', '#15882e', '#ffd962']
moreColor = ['#8b7530']
colorsD = ['#007b99', '#bee2e9']
fontsize = 10
markersize = 5
gridcolor = 'grey'
pagewidth = 5.78740290403
pageheight = 8.2440894208

plt.rc('font', size=fontsize, family='sans-serif')
plt.rc('xtick', labelsize=fontsize)
plt.rc('ytick', labelsize=fontsize)
plt.rc('axes', labelsize=fontsize)
plt.rc('legend', fontsize=fontsize)
plt.rc('lines', linewidth=0.5, linestyle='-', markersize=5)




def plotsAll():

    #convTest()
    associationEnergies()
    deltaE()
    raman_spectra()
    docking()

def ramanMethod():
    
    print("reading Raman spectra")
    with open('Daten/ramanMethod.pkl', 'rb') as f:
        data = pickle.load(f)
    
    Rcolors = colors + moreColor
    
    print('plot raman data')
    plt.figure(figsize=(pagewidth, 0.3*pageheight))
    for method,color in zip(data, Rcolors):
        plt.plot(*data[method]["dat"], label=method.replace('2','$^{2}$'), color=color)
    plt.xlim([0,2100])
    plt.xlabel(r'$\bar{\nu}$ [cm\textsuperscript{-1}]')
    plt.yticks([])
    plt.legend()
    plt.savefig(dest_path+'ramanMethod.png', dpi = 800)
    plt.show()
    plt.close()

def basisSets():
    
    data = pd.read_csv(data_path+'/basissetE.csv')
     
    
    plt.figure(1, figsize=(pagewidth,0.3*pageheight))
    plt.scatter(data["basis set"], data["$\Delta E_\\text{el}$"])
    plt.ylabel("$E_\\text{el}-E_\\text{el}(\\text{QZVPP}) $")
    plt.savefig(dest_path+'basissetE.png')
    plt.show()
    plt.close()

def docking():
    print("reading docking data")
    data=[]
    for clustersize in [str(c) for c in clusterSizes]:
        frame = pd.read_csv(data_path+'/docking/'+clustersize+'.csv')
        data.append(frame)
    numbers = [0,1,2,3]
    
    offset = 100
    
    print('ploting docking')
    fig, axes = plt.subplots(4,2, figsize=(pagewidth, pageheight))
    for clustersize, ax, frame in zip([str(c) for c in clusterSizes], axes.ravel(), data):
        print(clustersize, end=' ')
        ax.set_title(clustersize, y=0.8)
        for n, model, color in zip(numbers, models, colors):
            ax.scatter(frame['PBE Nr'], 
                    frame['\DE{int}{el,GFN_FF}'], 
                    label='GFN-FF',
                    color=colorsD[1])
            ax.scatter(frame['PBE Nr'], 
                    frame['\DE{int}{el,PBE}'], 
                    label='PBE',
                    color=colorsD[0])

    fig.supylabel(r'$\Delta_\text{int} E_\text{el}$')
    fig.supxlabel('Nr', y=0.05)
    
    print()
    # one legend with just the two entries
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    handles = handles[:2]
    labels = labels[:2]
    fig.legend(handles, labels,
               loc='lower center',
               ncol=2,
               bbox_to_anchor=(0.5, 0.00))   
    plt.savefig('../einkleben/Auswertung/AlH3/docking.png', dpi=800)
    plt.show(fig)

def raman_spectra():
    print("reading Raman spectra")
    with open('Daten/raman/spectra.pkl', 'rb') as f:
        spectra = pickle.load(f)
    
    numbers = [0,1,2,3]
    
    offset = 100
    
    print('ploting raman spectra')
    fig, axes = plt.subplots(2,4, figsize=(pageheight, 0.8*pagewidth))
    for clustersize, ax in zip([str(c) for c in clusterSizes], axes.ravel()):
        print(clustersize, end=' ')
        ax.set_title(clustersize, y=0.8)
        for n, model, color in zip(numbers, models, colors):
            ax.plot(spectra[model][clustersize][0], 
                    spectra[model][clustersize][1]+(3-n)*offset+20, 
                    label=model,
                    color=color)
            ax.set_ylim([0,1000])
            ax.set_xlim([0,2100])
            # remove y-ticks and labels
            ax.set_yticks([])
            ax.set_yticklabels([])
            
    fig.supylabel(r'Intensity', x=0.09)
    fig.supxlabel(r'$\nu$ [cm\textsuperscript{-1}]', y=0.02)
    
    print()
    # create one legend for the whole figure
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='lower center',
        ncol=len(models),
        bbox_to_anchor=(0.5, -0.05)  # adjust vertical spacing
    )    
    plt.savefig('../einkleben/Auswertung/AlH3/ramanSpectra_pre.png', dpi=800)
    plt.show(fig)



def associationEnergies():
    association = pd.read_csv(data_path+'/asEelm.csv')

    fig, ax = plt.subplots(figsize=(pagewidth, pageheight/2))

    handles = []
    labels = []
    for model, color in zip(models, colors):
        sc = ax.scatter(association['n'], association[model], 
                        label=model, color=color)
        handles.append(sc)
        labels.append(model)

    # One combined legend
    ax.legend(handles, labels, fontsize=fontsize, loc="best", frameon=False)

    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\Delta_\text{assoc} E_\text{el}$ [kJ mol$^{-1}$]")

    # Grid, but light
    ax.grid(True, color=gridcolor, linestyle=":", linewidth=0.5)

    # Save with exact figure size
    fig.savefig(dest_path+"/AlH3/asEelm.png", dpi=400, bbox_inches="tight")
    plt.close(fig)

def deltaE():
    data = pd.read_csv(data_path+'/deltaE.csv')
    
    
    Ecolors = (colors + moreColor)[1:]
    
    fig, ax = plt.subplots(figsize=(pagewidth, pageheight/2))

    handles = []
    labels = []
    procs = data.keys().to_list()
    procs.remove('n')
    print(procs)
    for proc, color in zip(procs, Ecolors):
        sc = ax.scatter(data['n'], data[proc], 
                        label=proc, color=color)
        handles.append(sc)
        labels.append(proc)

    # One combined legend
    ax.legend(handles, labels, fontsize=fontsize, loc="best", frameon=False)

    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\Delta E_\text{el}$ [kJ mol$^{-1}$]")

    # Grid, but light
    ax.grid(True, color=gridcolor, linestyle=":", linewidth=0.5)

    # Save with exact figure size
    fig.savefig(dest_path+"/AlH3/deltaE.png", dpi=400, bbox_inches="tight")
    plt.close(fig)
    

def convTest(): 
    
    ecutwfc = pd.read_csv(data_path+'ecut.csv')
    ecutrho = pd.read_csv(data_path+'ecutrho.csv')
    kpoints = pd.read_csv(data_path+'k-grid.csv')
    
    
    fig, axes = plt.subplots(1,3, figsize=(6,2), sharey=True )
    
    for ax,parameter in zip(axes,[ecutwfc, ecutrho, kpoints]):
        ax.scatter(parameter['parameter'][1:], parameter["lgDeltaE_per_at"][1:], color=colors[0], )
    axes[0].set_ylabel('$\lg(\Delta E / \\text{meV at}^{-1})$')
    axes[0].set_xlabel("ECutWFC [Ry]")
    axes[1].set_xlabel("ECutRho [150 Ry]")
    axes[2].set_xlabel("$n$(\\textsc{Monhorst-Pack})")    
    
    
    plt.savefig("/home/mehlhorn/mnt/TUBAF_home_drive/_Diplomarbeit/einkleben/Auswertung/mof/conv.png", dpi=800)
    plt.show()
    plt.close(fig)
    
    print("Convergence tests plotted")

if __name__ == "__main__":
    deltaE()
    print('done plots')