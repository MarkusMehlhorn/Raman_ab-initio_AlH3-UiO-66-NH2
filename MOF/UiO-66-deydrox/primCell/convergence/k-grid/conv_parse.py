import os
import numpy as np
from ase.units import Ry, eV
from matplotlib import pyplot as plt
parameters = [ f.name for f in os.scandir() if f.is_dir() ]
parameters.remove('.idea')
parameters.remove('template')

parameterrange=[]

for parameter in parameters:
    parameterrange.append(int(parameter))

parameterrange.sort()
print(parameterrange)

E=[]

for parameter in parameterrange:
    os.chdir(str(parameter))
    with open("pw.out", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if "!    total energy" in lines[i]:
            E.append(float(lines[i].split()[4]))
    print(E)
    os.chdir('..')

DeltaE=[]
print(parameterrange)
print(E)
for i in range(len(parameterrange)):
    if i==0:
        DeltaE.append(0)
    else:
        DeltaE.append(E[i]-E[i-1])

DeltaE_meVperat = eV*1e3/Ry*np.array(DeltaE)/22
lgDeltaE_meVperat=np.log10(np.absolute(DeltaE_meVperat))


print(parameterrange)
print(E)
print(DeltaE)
print(DeltaE_meVperat)
print(Ry)
print(eV)

plt.scatter(parameterrange, lgDeltaE_meVperat)
plt.ylabel('$lg(|\Delta E| [meV/at]^{-1})$')
plt.xlabel('$E_{cut,rho}$ [Ry]')
plt.xlim(left=2)
plt.savefig('conv_k.png')

table = np.array([parameterrange, DeltaE, DeltaE_meVperat])
np.savetxt('conv_parameter.txt', np.transpose(table))
