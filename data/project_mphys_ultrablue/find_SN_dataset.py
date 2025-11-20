import pandas as pd
import re
from collections import defaultdict

# --- File paths ---
csv_paths = {
    "prism": "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_prism.csv",
    "g140m": "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_g140m.csv",
    "g235m": "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_g235m.csv",
    "g395m": "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_g395m.csv",
    "g395h": "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_g395h.csv",
}

# --- Helper to extract object ID (trailing digits before ".spec.fits") ---
id_pattern = re.compile(r"_(\d+)\.spec\.fits$", re.IGNORECASE)
any_digits_pattern = re.compile(r"(\d+)(?!.*\d)")  # last group of digits in the string

def extract_id(filename):
    """Return the trailing numeric object ID for filenames like ..._35295.spec.fits.
       Fallback: return the last group of digits found in the string.
       Returns None if no digits found.
    """
    if pd.isna(filename):
        return None
    s = str(filename).strip()
    if not s:
        return None
    m = id_pattern.search(s)
    if m:
        return m.group(1)
    m2 = any_digits_pattern.search(s)
    return m2.group(1) if m2 else None


# -----------------------------------------------------------------------------
# Dictionaries mapping object_id -> set(gratings) for each line
heii1640_map = defaultdict(set)   # object_id -> set of gratings where HeII 1640 appears
heii4687_map = defaultdict(set)   # object_id -> set of gratings where HeII 4687 appears
ha_map      = defaultdict(set)    # object_id -> set of gratings where Ha_6565 appears
# -----------------------------------------------------------------------------

# Scan all CSVs and populate maps
for grating, path in csv_paths.items():
    try:
        df = pd.read_csv(path, dtype=str)  # read as strings to preserve formatting
    except FileNotFoundError:
        print(f"Warning: file not found: {path} — skipping {grating}")
        continue

    # He II 1640
    if "HeII_1640_SN" in df.columns:
        for raw in df["HeII_1640_SN"].dropna().astype(str):
            obj_id = extract_id(raw)
            if obj_id:
                heii1640_map[obj_id].add(grating)

    # He II 4687
    if "HeII_4687_SN" in df.columns:
        for raw in df["HeII_4687_SN"].dropna().astype(str):
            obj_id = extract_id(raw)
            if obj_id:
                heii4687_map[obj_id].add(grating)

    # H alpha 6565
    if "Ha_6565_SN" in df.columns:
        for raw in df["Ha_6565_SN"].dropna().astype(str):
            obj_id = extract_id(raw)
            if obj_id:
                ha_map[obj_id].add(grating)

# -----------------------------------------------------------------------------
# Build final table: include only objects that have at least one HeII (either)
# and at least one Ha detection.
all_heii_ids = set(heii1640_map.keys()) | set(heii4687_map.keys())
all_ha_ids   = set(ha_map.keys())

# IDs satisfying "at least one HeII and at least one Ha"
valid_ids = sorted(all_heii_ids & all_ha_ids)

print(f"Total HeII 1640 objects found: {len(heii1640_map)}")
print(f"Total HeII 4687 objects found: {len(heii4687_map)}")
print(f"Total Halpha objects found: {len(ha_map)}")
print(f"Objects with at least one HeII and at least one Halpha: {len(valid_ids)}")

# Build records
records = []
for obj_id in valid_ids:
    records.append({
        "object_id": obj_id,
        "HeII_1640_gratings": ",".join(sorted(heii1640_map.get(obj_id, []))) or "",
        "HeII_4687_gratings": ",".join(sorted(heii4687_map.get(obj_id, []))) or "",
        "Ha_6565_gratings": ",".join(sorted(ha_map.get(obj_id, []))) or "",
    })

# Save final CSV
output_path = (
    "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/"
    "data/project_mphys_ultrablue/HeII_Ha_high_SNR_allgratings.csv"
)
out_df = pd.DataFrame(records)
out_df.to_csv(output_path, index=False)

print(f"Saved {len(out_df)} rows to: {output_path}")
if len(out_df) > 0:
    print(out_df.head().to_string(index=False))
else:
    print("No matches found (no objects with both HeII and Ha detected).")
