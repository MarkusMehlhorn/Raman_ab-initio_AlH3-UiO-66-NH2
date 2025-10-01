
import os
from ase import io
import pandas as pd
from matplotlib import pyplot as plt
from ase import io
from ase.units import kJ, Ha, mol

base_dir = os.getcwd()
print(base_dir)

confs = range(16)

host = io.read('/home/mehlhorn/MOF/UiO-66-deydrox/sbu/GeomOpt/tight/orca.out', index=-1, format='orca-output')
Ehost = host.get_total_energy()
print("Ehost", Ehost)

cluster = io.read('/home/mehlhorn/(AlH3)n/vacGeom/5/calc/orca.out', index=-1, format='orca-output')
Ecluster = cluster.get_total_energy()
print("Ecluster", Ecluster)

print("sep", Ecluster + Ehost)

structures = []

# input
for i in confs:
    ind = str(i)
    print(i)
    atoms = io.read('./1/'+ind+'/orca.out', index=-1, format='orca-output')
    structures.append(atoms)

etot = []

for i in confs:
    etot.append(structures[i].get_total_energy())

data = {'Nr':confs, 'Etot':etot}
frame = pd.DataFrame(data)
frame["Eint"] = frame["Etot"] - Ehost - Ecluster
frame["Eint[kJ/mol]"]=frame["Eint"]/kJ*mol
frame = frame.sort_values(by="Etot")
frame["Sort-Nr"]=confs
print(frame)

plt.figure()
plt.scatter(frame["Sort-Nr"], frame["Eint[kJ/mol]"])
plt.ylabel('interaction energy [kJ/mol]')
plt.xlabel('enrgy hirachy')
plt.savefig("energies.png", dpi=600)
plt.close()

frame.to_csv('energies.csv')

