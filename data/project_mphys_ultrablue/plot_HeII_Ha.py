import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Load data ===
df = pd.read_csv("catalog-flux.csv")

# === Extract relevant columns ===
x = df["Ha_6565_SN"]
y = df["HeII_1640_SN"]

# === Clean data: remove NaN or infinite values ===
mask = np.isfinite(x) & np.isfinite(y)
x = x[mask]
y = y[mask]

# === Make the plot ===
plt.figure(figsize=(6,6))
plt.scatter(x, y, alpha=0.7, s=30)
plt.xlabel("Hα (6565 Å) SNR")
plt.ylabel("He II (1640 Å) SNR")
plt.title("He II vs Hα SNR")
plt.grid(True, linestyle="--", alpha=0.4)

# Add 1:1 reference line (only if there are valid points)
if len(x) > 0 and len(y) > 0:
    lims = [0, max(x.max(), y.max())]
    plt.plot(lims, lims, 'k--', alpha=0.6)
    plt.xlim(lims)
    plt.ylim(lims)

plt.tight_layout()

# === Save figure ===
out_fig = "HeII_vs_Ha_SNR.png"
plt.savefig(out_fig, dpi=300)
print(f"Saved figure as: {out_fig}")
