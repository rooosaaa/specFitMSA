import pandas as pd
import os

# --- File paths ---
combined_csv = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/uv_snr5plus_with_prism_and_medium.csv"
exposures_csv = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/src/mphys_GOODS_S_exposures.csv"

# Output directory
out_dir = "/nvme/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/src/"
os.makedirs(out_dir, exist_ok=True)

# --- Load data ---
combined = pd.read_csv(combined_csv)
exposures = pd.read_csv(exposures_csv)

# --- Function to build PROG_ID ---
def build_prog_id(row):
    root = row['root']
    srcid = str(row['srcid'])
    if "-" in root:
        root_base = "-".join(root.split("-")[:-2])
    else:
        root_base = root
    return f"{root_base}-{srcid}".upper()


# --- Define gratings, corresponding file columns, and filters ---
grating_info = {
    "PRISM": {"col": "prism_file", "filter": "CLEAR"},
    "G140M": {"col": "g140m_file", "filter": "F070LP"},
    "G235M": {"col": "g235m_file", "filter": "F170LP"},
    "G395M": {"col": "g395m_file", "filter": "F290LP"},
    "G395H": {"col": "g395h_file", "filter": "F290LP"},
}

# --- Loop over each grating and build CSV ---
for grating_label, info in grating_info.items():
    file_col = info["col"]
    filt = info["filter"]

    # Skip if that column doesn’t exist
    if file_col not in combined.columns:
        continue

    # Extract rows that have a file listed for this grating
    subset = combined.dropna(subset=[file_col]).copy()
    subset = subset.rename(columns={file_col: "file"})

    # Merge with exposures to get coords, etc.
    merged = subset.merge(exposures, on="file", how="left")

    if merged.empty:
        print(f" No matches found for {grating_label}")
        continue

    # --- Build output DataFrame ---
    output = pd.DataFrame({
        "Index": merged["srcid"],
        "PROG_ID": merged.apply(build_prog_id, axis=1),
        "Note": "",
        "z": merged.get("z", None),
        "file": merged["file"],
        "ra": merged["ra"],
        "dec": merged["dec"],
        "grating": grating_label,
        "filter": filt,
        "root": merged["root"]
    })

    # --- Save result ---
    out_csv = os.path.join(out_dir, f"matched_exposures_{grating_label.lower()}.csv")
    output.to_csv(out_csv, index=False)
    print(f"Saved {len(output)} rows → {out_csv}")

print("\nDone! All gratings processed.")
