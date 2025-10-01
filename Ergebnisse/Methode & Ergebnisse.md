# AlH3 cluster

## Benchmark Functionals and Basissets
- Testsystem: (AlH3)3
- Bechmark Method: MP2/auc-cc-pVTZ
- Methoden
	- PBE/pc-\[0-5]
	- r2SCAN-3c
- optimize (AlH3)n clusters
	- GOAT conf search
		- test on (AlH3)5, GFN2
		- 108 Geometries
		- global opt has different structure
## Create Geometries

### initial geometries 
- build Majzoub2011 in Avogadro
- optimize with UFF
- bei AlH3-8 lässt sich ein H nicht zuordnen.
	- Der in der Mitte ist völlig unbegründet.

### initial geom opt
- Geometry optimization of the build geometries from Majzoub2011
- level = PBE/pc-1
- porpose: get resonalble starting geometries for GFN-FF since it fixes bonds from the xyz input

### InitGeomOpt in vacuo (Stavila)
- build initial guess in Avogadro
- optimize with UFF
- optimize with PBE in ORCA
	- PBE pc-3 
- **can not reproduce the geometry of (AlNH3)8**
	- orientaded on Xu2013 (one H over)
	- MD for conformation search?
	- maybe it does not fit in the pores either
- **(AlH3)7 not reproducebile** 
	- Stavila has 1 H missing
	- building of my own guess
- launched all GeomOpt simultaneously

### Test GOAT and GFN
- (AlH3)5
- GOAT-EXPLORE with GFN2
- take geometries under 3 kcal/mol difference
- 6 Geometries optimized with PBE pc-2
	- global minimum extremely different
	- all structures similar
	- but different to the Stavila-structure

### Optimization with Linker
Tests on GFN2
- Aminotherephtalic acid
	- Cluster sticks to the carboxyl group
- Aminoparaxylol
	- cordination to amino group
- Rubidiumaminotherephtalate
	- cluster sticks to the carboxylate

*Compare coordination of Linker and SBU?*
- Cluster sticks to Oxygen

### docking
- GFN-FF
- 10 kcal/mol filter 

### post docking optimization
- all GFN-FF optimized structures
- PBE/def2-SV(P)
- soloppyOpt
- normalSCF
- DefGrid2


## Energies
### Cluster formation energies
### Interaction Energies
"Solvations energies"
"Interaction energies with the cluster"
- solvation
	- monotonic decrease with size
	- below 10 kJ/mol
	- see above surface to volume ratio
- interaction
	- not monotone
	- largest share
	- Geometry dependent
		- different fit 
		- 1,2,3 H-Zr, Al-O 2 centers
		- 4 H-Zr, Al-O 1 center
		- 5: H-Zr, Al-O, Al-O 2. zentrum
		- 6: Al-O, Zr....H
		- 7: O-Al-O
		- 8: H-Zr, Al-O, Al-O
	- strong dative bonding
	- 

## Raman-spectra

- Al-H Streckschwingungen bei ca 2000 cm^-1 verschieben zu niedrigeren Frequenzen mit sbu und solv
	- Warum?
	- solv: stabilizing of charge division 
	- sbu: weakening of bonds by coordination
- Al-H-Al vibration in a double bridge 1560
	- 2 and 5
- Al-H-Al bending ca. 1100
	- occuring at 3
- H-Al-H bending ca. 800
- 
- 
- g
	- 4
		- breathing 824
		- Al-H-Al bending 1020, 1073 cm^-1 
	- 5
		- brething 850 cm^-1 
		- Al-H-Al 1117,1139 cm^-1 
	- 6
		- Al-H-Al bending 1079, 1111, 1128, 1138, 1159
		- 

- sbu
	- 8 
		- Zr-H-Al 1559 cm^-1 
		- Al-O-C 847 cm^-1 
	- 7
		- Al-O-C 1338 cm^-1 
		- Al-O-C 807 cm^-1  
		- Al-H-Al bending 1189, 1134 cm^-1 

# MOF-Rechnungen
## UiO-66
### Struktur
- generiert aus UiO-66_?? aus der Literatur, experimentell mit Wasserstoff
	- UiO-66_0 aus der Analyse 688 Atoms/uc
- doppelte Sauerstoffatome entfernt
	- UiO-66_edit1 440 Atome/EZ
- Symmetrie entfernt
	- UiO-66_edit2 440 Atome/EZ
- Symmetrie auf niedrigste cubische P 2 3
	- 440 Atome/EZ
- Symmetrie auf F m -3 m
	- UiO-66_ready 440 Atome/EZ
	- *Warum generiert cif2cell nur 110 Atome*
- H durch N ersetzt, abgeleitet von UiO-66 P 2 3 
	- 440 Atme/EZ
- automatisch mit H abgesättigt
	- 488 Atome/EZ
- **SBU NICHT PROTONIERT!!!**
- Schwalbe
	- Strukturen für UiO-66 in WS-Zelle und Einheitszelle
### Symetrie
- output mit ase.io zu cif
- cif über aflow-sym zu sym.cif
- Vesta
- über cif2qe zum input.


### Rechnungen
- Kommentare im QE-Input
- 1. Versuch nicht konvergiert
- Kommentar Kortus: 
	- Höheres Cutoff Trepte 80 Ry
	- ecutrho x6
	- gamma sollte reichen
	- mit UiO-66 anfangen und dann die -NH2 ableiten
- Für UiO-66 test calculations:
	- single point at gamma in 3 min
	- dielectric constant at gamma in ca 5 h 
```         
Dielectric constant in cartesian axis    
  
         (       2.139651938       0.000000000      -0.000000000 )  
         (      -0.000000000       2.139651938      -0.000000000 )  
         (       0.000000000       0.000000000       2.139648980 )  
  
    Polarizability (a.u.)^3                    Polarizability (A^3)  
  1023.70     -0.00      0.00           151.6970       -0.0000        0.0000  
     0.00   1023.70      0.00             0.0000      151.6970        0.0000  
    -0.00     -0.00   1023.70            -0.0000       -0.0000      151.6967  
  
         Effective charges (d Force / dE) in cartesian axis without acoustic sum rule applied (asr)
```

## UiO-66 dehydrox.
### Struktur
- Aus Valenzano input parsen
	- selbst geschriebene Funktion CRYSTALinput --> structure object
	- structure --> ase.atoms
	- ase atoms --> cif
	- symmetrie hinzugefügt
		- raumgruppe und symmetrie operationen (aus einem (Falschen) Vesta output kopiert)
- Geometrie optimieren
	- 80 Ry, econv = 3,2 10^-6 , econvscf=10^-8, force conv = 10^-5  
	- ```bfgs failed after   4 scf cycles and   2 bfgs steps, convergence not achieved```
	- Kortus: force conv zu strickt, 10^-3 ausreichend
	- --> converged
- Dielektrizitätskonstante berechnet
noSym
```
          (       2.130266210      -0.037986906      -0.027217846 )
          (      -0.037986922       2.171216116      -0.016248172 )
          (      -0.027217884      -0.016248373       2.182264763 )
```
Sym
```
          (       2.192899812      -0.000000033       0.000000000 )
          (       0.000000033       2.192899812       0.000000000 )
          (      -0.000000000       0.000000000       2.095767444 )
```
## UiO-66-NH2-dehydrox
### Struktur
- aus der selbst optimierten Valenzano-Struktur ableiten
- In VESTA H durch stickstoff ersetzen
- Struktur Mercury übergeben und automatisch Wasserstoff ergänzen
- Geometrieoptimierung
	- converged
- Dielectric constant
Sym
```
		(       2.324795853      -0.000000002       0.000000000 )
        (       0.000000002       2.324795853       0.000000000 )
        (      -0.000000000       0.000000000       2.219772997 )
```


## Dielectric constants \epsilon
- code epsilon.x
	- learn theory!
- functional
	- HSE? read about!
- calculation parameters
	- ecutwfc/ecurho
		- 100, 150 no difference


# Writing notes

- Begriff aggregate
- Begriff conformation
- resolution of Avogadro PNGs
- Association energy picture
	- plot interaction term
- Write about the study on 


# Conclusion & Outlook

- preferred adsorption site?
	- systematic studies on the linker are necessary
- dielectric constant on high level of theory
- Interaction
	- explicit interaction dominates
	- interaction term inconsistent
	- PES of PBE and GFN-FF extremely different. 
		- Docking study with an better method 
- Computation of UiO-66 feasible even without using symmetry
- Combination of solid state calculations with molecular calculations