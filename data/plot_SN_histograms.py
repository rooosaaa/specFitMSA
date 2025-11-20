import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- CONFIG ----------------------
csv_path = "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/catalog-flux_g395h.csv"
output_path = "sn_histogram_g395h.png"
grating_name = "Grating: G395H"  # replace with the appropriate grating if needed
output_csv = "/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/sn_above2_files_g395h.csv"

# ---------------------- LOAD DATA ----------------------
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# ---------------------- BASE COLUMNS ----------------------
sn_cols = ['HeII_4687_SN', 'Ha_6565_SN']
# Include HeII_1640_SN only if it exists
if 'HeII_1640_SN' in df.columns:
    sn_cols.insert(1, 'HeII_1640_SN')  # insert it between 4687 and Ha

# ---------------------- FIND UNRESOLVED VARIANTS ----------------------
extra_sn_cols = [
    c for c in df.columns
    if c.endswith('_SN')
    and c not in sn_cols
    and any(tag in c for tag in ['HeII_4687', 'HeII_1640', 'Ha_6565'])
]

# Combine all relevant columns for plotting
all_sn_cols = sn_cols + extra_sn_cols

# ---------------------- COUNT OBJECTS ABOVE THRESHOLDS ----------------------
print("\nNumber of objects with S/N > 2 and S/N > 3:")
for col in sn_cols:
    if col in df.columns:
        count_gt2 = (df[col] > 2).sum()
        count_gt3 = (df[col] > 3).sum()
        print(f"{col:15s}  >2: {count_gt2:5d}   >3: {count_gt3:5d}")
    else:
        print(f"{col:15s}  (column not found)")

# ---------------------- FIND OVERLAPS ----------------------
# Create masks only for columns that exist
mask = {col: df[col] > 2 for col in sn_cols if col in df.columns}
sets = {col: set(df.loc[mask[col], 'file']) for col in mask}

# Safely compute overlaps
both_heii = sets.get('HeII_4687_SN', set()) & sets.get('HeII_1640_SN', set())
both_heii_ha = sets.get('HeII_4687_SN', set()) & sets.get('Ha_6565_SN', set())
both_1640_ha = sets.get('HeII_1640_SN', set()) & sets.get('Ha_6565_SN', set())
all_three = sets.get('HeII_4687_SN', set()) & sets.get('HeII_1640_SN', set()) & sets.get('Ha_6565_SN', set())


print("\nFiles with S/N > 2 in multiple lines:")
print(f"- HeII 4687 & HeII 1640 overlap: {len(both_heii)} objects")
print(f"- HeII 4687 & Hα 6565 overlap:   {len(both_heii_ha)} objects")
print(f"- HeII 1640 & Hα 6565 overlap:   {len(both_1640_ha)} objects")
print(f"- All three lines overlap:       {len(all_three)} objects\n")

# Print overlapping files
if all_three:
    print("Files with S/N > 2 in ALL THREE lines:")
    for f in sorted(all_three):
        print("  ", f)

# Print filenames for overlaps
if both_heii:
    print("HeII 4687 & HeII 1640 overlap files:")
    for f in sorted(both_heii):
        print("  ", f)
    print()

if both_heii_ha:
    print("HeII 4687 & Hα 6565 overlap files:")
    for f in sorted(both_heii_ha):
        print("  ", f)
    print()

if both_1640_ha:
    print("HeII 1640 & Hα 6565 overlap files:")
    for f in sorted(both_1640_ha):
        print("  ", f)
    print()

if all_three:
    print("Files with S/N > 2 in ALL THREE lines:")
    for f in sorted(all_three):
        print("  ", f)

# ---------------------- PLOT ----------------------

plt.figure(figsize=(8, 6))

# Plot both the main and unresolved versions if they exist
for col in all_sn_cols:
    plt.hist(
        df[col].dropna(),
        bins=100,
        range=(0, 30),
        alpha=0.6,
        label=col.replace('_SN', '')  # just the line name
    )

# Axis labels and title
plt.xlabel("Signal-to-Noise Ratio (S/N)", fontsize=18)
plt.ylabel("Number of Objects", fontsize=18)
plt.title("Distribution of S/N for HeII and Hα Lines", fontsize=18)

# Legend with grating name as title
plt.legend(title=grating_name, fontsize=14, title_fontsize=16)

# Tick label sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.xlim(0, 30)

plt.grid(alpha=0.3)
plt.tight_layout()



# ---------------------- SAVE ----------------------
plt.savefig(output_path, dpi=300)
plt.close()

print(f"\nHistogram saved to: {output_path}\n")

# ---------------------- GET FILES ABOVE S/N > 2 ----------------------
files_above2 = {col: df.loc[df[col] > 2, 'file'].tolist() for col in sn_cols}

# ---------------------- CREATE A DATAFRAME ----------------------
# We make a DataFrame with one column per emission line
max_len = max(len(lst) for lst in files_above2.values())
data = {}
for col, lst in files_above2.items():
    # pad shorter lists with empty strings
    data[col] = lst + ['']*(max_len - len(lst))

out_df = pd.DataFrame(data)

# ---------------------- SAVE TO CSV ----------------------
out_df.to_csv(output_csv, index=False)
print(f"Saved filenames with S/N > 2 to: {output_csv}")
