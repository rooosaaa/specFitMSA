import os
from astropy.io import fits

# Folder containing the FITS files
folder = "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/pymc_outputs_prism"

# Column we're looking for
target_column = "HeII_4687_NeIV_4714_NeIV_4725_OIII_4959"

# Loop through all FITS files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".fits"):
        filepath = os.path.join(folder, filename)
        try:
            with fits.open(filepath) as hdul:
                # Usually the first table HDU is at index 1
                columns = hdul[1].columns.names
                if target_column in columns:
                    print(f"FOUND in: {filename}")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
