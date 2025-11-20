import os
from pathlib import Path

# Define the target folder
folder = Path("/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/pymc_outputs_prism")

# Loop through files in the folder
for file in folder.iterdir():
    if file.is_file() and "Ha_6565" in file.name:
        print(f"Removing: {file}")
        file.unlink()  # deletes the file

print("Done.")