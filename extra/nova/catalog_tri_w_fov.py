import pandas as pd
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import itertools
import os
from tqdm import tqdm  # pip install tqdm

# ---------------- CONFIG ----------------
catalog_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\filtered_stars_38.csv"
wcs_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\wcs.fits"
image_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\new-image.fits"
output_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\catalog_tri_w_fov.csv"

EDGE_FACTOR = 1.05        # small margin beyond exact FOV
MAX_HPMAG = 3.8           # optional filter to only include brighter stars
# ----------------------------------------

# Load catalog
catalog = pd.read_csv(catalog_file)
print(f"Loaded {len(catalog)} stars from catalog.")

# Filter by magnitude if desired
catalog = catalog[catalog["Hpmag"] <= MAX_HPMAG].reset_index(drop=True)
print(f"{len(catalog)} stars after magnitude filter (Hpmag <= {MAX_HPMAG})")

# RA is radians, Dec is already degrees
ra_deg = np.degrees(catalog["RArad"].values)
dec_deg = catalog["DErad"].values

# Load WCS
if not os.path.exists(wcs_file):
    raise FileNotFoundError(wcs_file)

hdul = fits.open(wcs_file)
hdr = hdul[0].header
wcs = WCS(hdr)

# Determine image size
if hasattr(wcs, "pixel_shape") and wcs.pixel_shape is not None:
    nx, ny = wcs.pixel_shape
else:
    try:
        img_hdul = fits.open(image_file)
        nx = img_hdul[0].header["NAXIS1"]
        ny = img_hdul[0].header["NAXIS2"]
    except KeyError:
        raise RuntimeError("WCS does not contain pixel_shape or NAXIS1/NAXIS2. Please provide image size.")

print(f"Image size: {nx} x {ny} pixels")

# Compute diagonal FOV
corners = np.array([[0, 0], [nx, 0], [0, ny], [nx, ny]], dtype=float)
corners_world = wcs.all_pix2world(corners, 0)

c1 = SkyCoord(corners_world[0, 0] * u.deg, corners_world[0, 1] * u.deg)
c2 = SkyCoord(corners_world[3, 0] * u.deg, corners_world[3, 1] * u.deg)
diag_fov = c1.separation(c2).rad * EDGE_FACTOR
print(f"Diagonal FOV: {np.degrees(diag_fov):.3f} deg")

# Build SkyCoord for catalog
coords = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame="icrs")

# Build triangles with progress bar
rows = []
comb_iter = itertools.combinations(range(len(coords)), 3)
total_combinations = int(len(coords)*(len(coords)-1)*(len(coords)-2)/6)

print(f"Generating up to {total_combinations} triangles...")
for i, j, k in tqdm(comb_iter, total=total_combinations, desc="Processing triangles"):
    s12 = coords[i].separation(coords[j]).rad
    s23 = coords[j].separation(coords[k]).rad
    s31 = coords[k].separation(coords[i]).rad
    if max(s12, s23, s31) <= diag_fov:
        rows.append({
            "i1": i, "i2": j, "i3": k,
            "HIP1": catalog.iloc[i]["HIP"],
            "HIP2": catalog.iloc[j]["HIP"],
            "HIP3": catalog.iloc[k]["HIP"],
            "s12_rad": s12,
            "s23_rad": s23,
            "s31_rad": s31
        })

# Save triangles
tri_df = pd.DataFrame(rows)
tri_df.to_csv(output_file, index=False)
print(f"Saved {len(tri_df)} valid triangles to {output_file}")
