import shutil
from pathlib import Path

# Source and destination folders
source_folder = Path("/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/pymc_outputs_prism_Ha_6565")
destination_folder = Path("/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/pymc_outputs_prism")

# Create destination folder if it doesn't exist
destination_folder.mkdir(parents=True, exist_ok=True)

# Move files
for file in source_folder.iterdir():
    if file.is_file():
        shutil.move(str(file), str(destination_folder / file.name))
        print(f"Moved: {file.name}")

print("All files moved successfully.")
