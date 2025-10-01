
import os
import numpy as np
from pwtools import thermo
from pwtools import io
from pwtools import crys
import scipy
from matplotlib import pyplot as plt
import pandas as pd



def gibbs():
    dospack = np.loadtxt('../calc/matdyn.dos')
    dospackt=np.transpose(dospack)
    #print(dospackt)
    freq=dospackt[0]
    #print(freq)
    dos=dospackt[1]
    #print(dos)
    
    structure = io.read_pw_scf('../calc/pw.out')
    print(structure)
    etot = structure.get_etot() # convert Rydberg to eV
    # get the cell constants in Bohr and convert them to Angstrom
    cell = structure.get_cryst_const() # convert Bohr to Angstrom
    cell_len=[cell[0],cell[1],cell[2]]
    
    
    
    Int=scipy.integrate.trapezoid(dos,freq)
    print(Int)
    
    im=scipy.integrate.trapezoid(dos[:3525],freq[:3525])
    print(im)
    print(im/Int)
    
    volfunc_ax = lambda x: crys.volume_cc([x[0],x[1],x[2],cell[3],cell[4],cell[5]])
    
    T=np.linspace(0, 500, 101)
    
    print(len(np.array([[freq,dos]])))
    print(np.array([cell]).shape[0])
    
    
    HT = thermo.Gibbs( phdos=np.array([[freq,dos]]),
                       T=T,
                       P=np.array([1e-4]),
                       etot=[etot],
                       axes_flat=np.array([cell_len]),
                       volfunc_ax=volfunc_ax,
                       case='1d',
                       temp=None,
                       skipfreq=True,
                       eps=3.3306690738754696e-16,
                       fixnan=True, 
                       nanfill=0.0,
                       dosarea=324,
                       integrator=scipy.integrate.simpson,
                       verbose=True)
    g=HT.calc_G(calc_all=False)
    
    
    
    #print(Cv)
    plt.figure('Cv')
    plt.plot(T, g['/ax0-ax1-ax2/T/Cv'][0]) 
    plt.savefig('../plots/Cv.png', dpi=500)
    plt.show()
    plt.close('Cv')
    
    plt.figure('dos')
    plt.plot(freq, dos, linewidth=0.3)
    plt.savefig('../plots/dos.png', dpi=500)
    plt.show()
    plt.close('dos')
    
    
    # pack data 
    
    data=pd.DataFrame({'T[K]':T, 'Cv[eV/mol/K]':g['/ax0-ax1-ax2/T/Cv'][0]})
    print(data)

def harmTherm():
    dospack = np.loadtxt('../calc/matdyn.dos')
    dospackt=np.transpose(dospack)
    #print(dospackt)
    freq=dospackt[0]
    #print(freq)
    dos=dospackt[1]
    #print(dos)

    
    
    
    Int=scipy.integrate.trapezoid(dos,freq)
    print(Int)
    
    im=scipy.integrate.trapezoid(dos[:3525],freq[:3525])
    print(im)
    print(im/Int)
    
    T=np.linspace(0, 20, 21)
    
    
    
    HT = thermo.HarmonicThermo(freq,
                               dos,
                               T=T,
                               temp=None,
                               skipfreq=True,
                               eps=3.3306690738754696e-16,
                               fixnan=True, 
                               nanfill=0.0,
                               dosarea=324,
                               integrator=scipy.integrate.simpson,
                               verbose=True)
    
    
    
    #print(Cv)
    plt.figure('Cv')
    plt.plot(T, HT.cv()) 
    plt.savefig('../plots/Cv.png', dpi=500)
    plt.show()
    plt.close('Cv')
    
    plt.figure('dos')
    plt.plot(freq, dos, linewidth=0.3)
    plt.savefig('../plots/dos.png', dpi=500)
    plt.show()
    plt.close('dos')
    
    
    # pack data 
    
    Cv=pd.DataFrame({'T[K]':T, 'Cv[eV/mol/K]':HT.cv()})
    print(Cv)
    Cv.to_csv('Cv.csv')
    
    dos=pd.DataFrame({'f[cm^-1]':freq, 'DOS':dos})
    print(dos)
    dos.to_csv('DOS.csv')
    
if __name__ == "__main__":
    harmTherm()

