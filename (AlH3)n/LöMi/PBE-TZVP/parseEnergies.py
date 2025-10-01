import os
import pandas as pd
import matplotlib.pyplot as plt
from ase.io import read
from ase.units import Hartree # Used for converting eV (ASE's default) to Hartrees

def parse_orca_energy_ase(filepath):
    """
    Parses an ORCA output file using ASE to get the electronic energy.

    Args:
        filepath (str): The full path to the ORCA output file.

    Returns:
        float: The final electronic energy in Hartrees, or None if parsing fails.
    """
    try:
        # ASE's `read` function is a powerful parser for many quantum chemistry formats.
        # By default, it reads the last configuration in the file, which contains
        # the final converged energy.
        atoms = read(filepath, format='orca-output')
        
        # The get_potential_energy() method returns the total electronic energy in eV.
        energy_ev = atoms.get_total_energy()
        
        # We convert the energy from eV back to Hartrees for consistency.
        # The `Hartree` constant from ase.units is the conversion factor (eV/Hartree).
        energy_hartree = energy_ev / Hartree
        
        return energy_hartree
        
    except FileNotFoundError:
        print(f"Warning: Output file not found at {filepath}")
    except Exception as e:
        # ASE can raise various errors if parsing fails (e.g., if the calculation
        # did not finish correctly).
        print(f"An error occurred while parsing {filepath} with ASE: {e}")
        
    return None

def EnergiesAlH3(source_path):
    """
    Main function to orchestrate the parsing, analysis, and exporting.
    """
    # --- Configuration ---
    # List of directory names. Assumes they are in the same folder as the script.
    dir_names = [str(i) for i in range(1, 9)]
    # path to Daten dir
    Daten_path='/home/mehlhorn/mnt/TUBAF_home_drive/_Diplomarbeit/Ergebnisse/Daten/'
    # The name of the ORCA output file in each directory.
    # ASE is smart enough to find the .out or .log file.
    output_filename = "orca.out" 
    
    # A list to hold the data extracted from the files.
    results = []

    print("Starting analysis of ORCA output files using ASE...")

    # --- Data Parsing ---
    # Loop through each directory.
    for dir_name in dir_names:
        # Construct the full path to the output file.
        file_path = os.path.join(source_path, dir_name, output_filename)
        
        print(f"Processing file: {file_path}")
        
        # Parse the energy from the file using our new ASE-based function.
        energy = parse_orca_energy_ase(file_path)
        
        if energy is not None:
            # If energy was found, add it to our results list.
            results.append({
                'n': int(dir_name),
                'Electronic Energy (Eh)': energy
            })
        else:
            print(f"Could not find energy in {file_path}. Skipping.")

    # --- Data Processing with Pandas ---
    if not results:
        print("No data was successfully parsed. Exiting.")
        return

    # Create a pandas DataFrame from the collected results.
    df = pd.DataFrame(results)
    
    # Calculate the new column as requested.
    df['$E_m$ Ha'] = df['Electronic Energy (Eh)'] / df['n']
    
    # Sort by system number just in case.
    df = df.sort_values(by='n').reset_index(drop=True)

    print("\n--- Processed Data ---")
    print(df)

    # --- Data Exporting ---
    # Export the DataFrame to a CSV file.
    csv_filename = 'clusterEnergies.csv'
    df.to_csv(Daten_path+csv_filename, index=False)
    print(f"\nData successfully exported to {csv_filename}")

    # Export the DataFrame to a LaTeX table file.
    latex_filename = 'electronic_energies_ase.tab'
    df.to_latex(latex_filename, 
                index=False, 
                caption='Calculated Electronic Energies from ORCA (parsed with ASE).',
                label='tab:energies_ase',
                position='h')
    print(f"Data successfully exported to {latex_filename}")

if __name__ == "__main__":
    # To run this script, you need to have ASE installed:
    # pip install ase
    source_path=os.path.dirname(os.path.abspath(__file__))
    parseEnergiesAlH3(source_path)