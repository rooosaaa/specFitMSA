import pandas as pd
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# --- Paths ---
galaxies_path = '/raid/scratch/work/rroberts/mphys_pop_III/ultrablue-galaxies-mphys/specFitMSA/data/project_mphys_ultrablue/matching_ids_sample.csv'
galaxies_df = pd.read_csv(galaxies_path)

south_cat_path = "/raid/scratch/work/Griley/GALFIND_WORK/Catalogues/v13/ACS_WFC+NIRCam/JADES-DR3-GS-South/(0.32)as/JADES-DR3-GS-South_MASTER_Sel-F277W+F356W+F444W_v13.fits"
east_cat_path  = "/raid/scratch/work/Griley/GALFIND_WORK/Catalogues/v13/ACS_WFC+NIRCam/JADES-DR3-GS-East/(0.32)as/JADES-DR3-GS-East_MASTER_Sel-F277W+F356W+F444W_v13.fits"

# --- Load catalogues ---
def load_objects_table(fits_path):
    with fits.open(fits_path) as hdul:
        return hdul['OBJECTS'].data

south_data = load_objects_table(south_cat_path)
east_data  = load_objects_table(east_cat_path)

# --- Compute colours and their errors for catalogues ---
def compute_colours_and_errors(data):
    # Fluxes
    F444W = data['MAG_APER_F444W']
    F410M = data['MAG_APER_F410M']
    F115W = data['MAG_APER_F115W']
    F150W = data['MAG_APER_F150W']
    # Magnitude errors
    F444W_err = data['MAGERR_APER_F444W']
    F410M_err = data['MAGERR_APER_F410M']
    F115W_err = data['MAGERR_APER_F115W']
    F150W_err = data['MAGERR_APER_F150W']
    
    # Colours
    colour1 = F410M - F444W
    colour2 = F115W - F150W
    
    # Propagated errors
    colour1_err = np.sqrt(F410M_err**2 + F444W_err**2)
    colour2_err = np.sqrt(F115W_err**2 + F150W_err**2)
    
    return colour1, colour2, colour1_err, colour2_err

# Compute for South and East
south_colour1, south_colour2, south_err1, south_err2 = compute_colours_and_errors(south_data)
east_colour1, east_colour2, east_err1, east_err2 = compute_colours_and_errors(east_data)

# --- Match sample galaxies and propagate errors ---
gal_colour1 = []
gal_colour2 = []
gal_err1 = []
gal_err2 = []

for idx, row in galaxies_df.iterrows():
    if not pd.isna(row['photo_id_south']):
        mask = south_data['NUMBER'] == row['photo_id_south']
        if np.any(mask):
            gal_colour1.append(south_colour1[mask][0])
            gal_colour2.append(south_colour2[mask][0])
            gal_err1.append(south_err1[mask][0])
            gal_err2.append(south_err2[mask][0])
    elif not pd.isna(row['photo_id_east']):
        mask = east_data['NUMBER'] == row['photo_id_east']
        if np.any(mask):
            gal_colour1.append(east_colour1[mask][0])
            gal_colour2.append(east_colour2[mask][0])
            gal_err1.append(east_err1[mask][0])
            gal_err2.append(east_err2[mask][0])

# Convert to numpy arrays
gal_colour1 = np.array(gal_colour1)
gal_colour2 = np.array(gal_colour2)
gal_err1 = np.array(gal_err1)
gal_err2 = np.array(gal_err2)

# --- Plot with error bars ---
plt.figure(figsize=(6,6))
plt.errorbar(gal_colour2, gal_colour1, xerr=gal_err2, yerr=gal_err1,
             fmt='o', markersize=6, color='blue', ecolor='gray', elinewidth=1,
             capsize=2, label='Sample Galaxies')

plt.xlabel('F115W - F150W [mag]')
plt.ylabel('F410M - F444W [mag]')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.title('JWST NIRCam Colour-Colour Diagram (Sample Galaxies) with Errors')

plt.savefig('sample_galaxies_colour_colour_errors.png', dpi=300, bbox_inches='tight')
plt.show()



