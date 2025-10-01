
import os
import numpy as np
from matplotlib import pyplot as plt
import re

def get_bands(file):
    
    bands = []
    with open(file, "r") as f:
        for line in f:
            match = re.match(r"\s*\d+\s+([\d.]+)\s+[\d.]+\s+([\d.]+)", line)
            if match:
                freq = float(match.group(1))
                raman = float(match.group(2))
                if raman > 0:  # Only keep Raman-active modes
                    bands.append((freq, raman))
    return bands


if __name__ == "__main__":
    
    
    methods = ["PBE0-DH", "PBE0", "PBE", "PBEh-3c", "r2SCAN-3c"]
    
    data = dict.fromkeys(methods)
    
    print('read raman.data')
    for method in methods:
        
        print(' '+method)
        data[method] = {}
        
        data[method]["dat"] = np.loadtxt(method+'/raman.dat').transpose()
    
    print('plot raman data')
    plt.figure(1)
    for method in methods:
        plt.plot(*data[method]["dat"], label=method)    
    plt.legend()
    plt.savefig('ramanSpect.png')
    plt.savefig('spec/plot.png', dpi = 800)
    plt.show()
    plt.close(1)
    
