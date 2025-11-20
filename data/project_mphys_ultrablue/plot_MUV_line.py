import pandas as pd
import matplotlib.pyplot as plt

# === Load your line flux catalog ===
df_lines = pd.read_csv("catalog-flux.csv")  # contains line fluxes and PROG_ID

# === Load your M_UV values ===
df_mag = pd.read_csv("magnitudes_UV_AB.csv")  # contains PROG_ID and M_UV

# === Merge the two on PROG_ID ===
df = pd.merge(df_lines, df_mag[['PROG_ID', 'M_UV']], on='PROG_ID', how='inner')

# === Select only your two target spectra ===
targets = ["GDS-199856", "GDS-201249"]
df_sel = df[df["PROG_ID"].isin(targets)]

# === Optional: require SNR > 3 for a specific line ===
line = "NeIV_1602_flux"    # the line flux column
sn_line = "NeIV_1602_SN"   # the SNR column, if you have it
df_sel = df_sel[df_sel[sn_line] > 3]  # keep only if SNR > 3

# === Plot with flipped axes ===
plt.figure(figsize=(6,4))
plt.scatter(df_sel[line], df_sel["M_UV"], s=80, c='darkblue')  # swap x and y

# Add labels for each point
for _, row in df_sel.iterrows():
    plt.text(row[line], row["M_UV"]*1.05, row["PROG_ID"], 
             ha='center', fontsize=8, color='darkred')

plt.gca().invert_yaxis()   # Brighter M_UV at top
plt.xlabel(f"{line} [Flux units]")
plt.ylabel(r"$M_{\mathrm{UV}}$")
plt.title(f"$M_{{UV}}$ vs. {line} Flux for Selected Targets")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("MUV_vs_line_flux_flipped.png", dpi=300)
plt.show()
