import pandas as pd
import matplotlib.pyplot as plt
import re

# === USER SETTINGS ===
csv_path = "catalog-flux.csv"   # input CSV
save_fig = True                 # set False to just show plot
out_fig = "flux_vs_snr_all_normalized.png" # output figure name
snr_threshold = 3.0             # SNR cut for reporting

# === LOAD DATA ===
df = pd.read_csv(csv_path)

# === FIND all line names (e.g. "HeII_1640", "OIII_1665") ===
flux_cols = [c for c in df.columns if c.endswith("_flux")]
snr_cols = [c for c in df.columns if c.endswith("_SN")]

# Extract the line roots (text before "_flux" or "_SN")
def line_root(col):
    return re.sub(r'_(flux|SN)$', '', col)

flux_lines = {line_root(c): c for c in flux_cols}
snr_lines  = {line_root(c): c for c in snr_cols}

# Lines present in both flux and SNR form
common_lines = sorted(set(flux_lines.keys()) & set(snr_lines.keys()))
print(f"Found {len(common_lines)} spectral lines: {common_lines}")

# === PLOT: Normalized Flux vs SNR for all lines ===
plt.figure(figsize=(8, 6))

for line in common_lines:
    flux = df[flux_lines[line]] / df["flux_norm"]  # normalize by flux_norm
    snr  = df[snr_lines[line]]

    plt.scatter(
        snr, flux,
        alpha=0.7, label=line, s=20
    )

plt.xlabel("Signal-to-Noise Ratio (SNR)")
plt.ylabel("Normalized Line Flux")
plt.title("Normalized Flux vs. SNR for All Unresolved Spectral Lines")
plt.legend(frameon=False, fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

if save_fig:
    plt.savefig(out_fig, dpi=300)
    print(f"Saved plot as {out_fig}")
else:
    plt.show()

# === REPORT: Sources with SNR > threshold for each line ===
print(f"\n=== Sources with SNR > {snr_threshold} ===")
for line in common_lines:
    sn_col = snr_lines[line]
    high_snr = df[df[sn_col] > snr_threshold]

    if not high_snr.empty:
        print(f"\n{line}: {len(high_snr)} sources exceed SNR > {snr_threshold}")
        print(high_snr[['PROG_ID', sn_col]].to_string(index=False))
    else:
        print(f"\n{line}: No sources with SNR > {snr_threshold}")
