import os
import matplotlib.pyplot as plt
import h5py
from synthesizer.grid import Grid
from synthesizer.emissions.line_ratios import get_ratio_label

# --- Paths and grids ---
grids_directory = '/nvme/scratch/work/tharvey/synthesizer/grids/'
grid_names = [
    'yggdrasil-1.3.3-POPIII-fcov_0.5_kroupa-0.1,100.hdf5',
    'yggdrasil-1.3.3-POPIII-fcov_0.5_salpeter-10,1,500.hdf5',
    'yggdrasil-1.3.3-POPIII-fcov_0.5_salpeter-50,500.hdf5',
    'yggdrasil-1.3.3-POPIII-fcov_1_kroupa-0.1,100.hdf5',
    'yggdrasil-1.3.3-POPIII-fcov_1_salpeter-10,1,500.hdf5',
    'yggdrasil-1.3.3-POPIII-fcov_1_salpeter-50,500.hdf5',
    'yggdrasil-1.3.3-PopIII_kroupa-0.1,100.hdf5',
    'yggdrasil-1.3.3-PopIII_salpeter-10,1,500.hdf5',
    'yggdrasil-1.3.3-PopIII_salpeter-50,500.hdf5'
]

# --- Select a grid ---
grid_name = 'yggdrasil-1.3.3-POPIII-fcov_0.5_kroupa-0.1,100.hdf5'

# --- Load the grid ---
grid = Grid(grid_name, grids_directory)
grid_path = os.path.join(grids_directory, grid_name)

file_path = "/nvme/scratch/work/tharvey/synthesizer/grids/yggdrasil-1.3.3-PopIII_salpeter-10,1,500.hdf5"

with h5py.File(file_path, 'r') as f:
    wavelengths = f['spectra/wavelength'][:]
    spectrum = f['spectra/incident'][:]  # shape probably (ages, metals, points)

# pick a single age and metallicity index to plot
age_idx = 0
metal_idx = 0
spec_to_plot = spectrum[age_idx, metal_idx, :]

plt.figure(figsize=(10, 6))
plt.plot(wavelengths, spec_to_plot)
plt.xlabel("Wavelength [Å]")
plt.ylabel("Luminosity [erg/s]")
plt.title("Sample Yggdrasil Spectrum")
plt.yscale("log")
plt.xscale("log")
plt.tight_layout()
plt.savefig("sample_spectrum.png")
plt.show()


