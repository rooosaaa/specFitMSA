import pandas as pd

# --- File paths ---
exposures_csv = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/src/mphys_GOODS_S_exposures.csv"
snr_csv = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/src/uv_snr_5plus.csv"
output_csv = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/src/matched_exposures_with_snr.csv"

# --- Load the CSVs ---
exposures = pd.read_csv(exposures_csv)
snr_data = pd.read_csv(snr_csv)

# --- Merge on 'file' column ---
merged = exposures.merge(snr_data, on="file", how="inner")

# --- Function to build PROG_ID ---
def build_prog_id(row):
    root = row['root']
    srcid = str(row['srcid'])
    
    # Remove everything after last underscore in root
    if "-" in root:
        root_base = "-".join(root.split("-")[:-2])
    else:
        root_base = root
    
    prog_id = f"{root_base}-{srcid}".upper()
    return prog_id

# --- Create output DataFrame ---
output = pd.DataFrame({
    "Index": merged["srcid"],
    "PROG_ID": merged.apply(build_prog_id, axis=1),
    "Note": "",
    "z": merged.get("z", None),
    "file": merged["file"],
    "ra": merged["ra"],
    "dec": merged["dec"],
    "grating": "PRISM",
    "filter": "CLEAR",
    "root": merged["root"]
})

# --- Save result ---
output.to_csv(output_csv, index=False)

print(f"Done! Saved {len(output)} matched rows to:\n{output_csv}")
