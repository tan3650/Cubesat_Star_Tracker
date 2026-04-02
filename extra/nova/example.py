import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from skimage.feature import peak_local_max
import itertools
import warnings
import matplotlib.pyplot as plt
from imageio import v2 as imageio

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------- CONFIG ----------------
image_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\bmp_4.bmp"
wcs_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\wcs.fits"
triangle_catalog_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\triangles_selected.csv"
star_catalog_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\filtered_stars_38.csv"
TOP_N_STARS = 50
ANGLE_TOL = 0.05  # radians for triangle matching
MIN_DISTANCE = 50   # pixels for peak_local_max
THRESHOLD = 70      # intensity threshold for star detection
# ----------------------------------------

# --- Load image ---
img = imageio.imread(image_file)
if img.ndim == 3:
    img = img[..., 0]

# --- Detect bright stars ---
coordinates = peak_local_max(img, min_distance=MIN_DISTANCE, threshold_abs=THRESHOLD)
if len(coordinates) > TOP_N_STARS:
    intensities = img[coordinates[:,0], coordinates[:,1]]
    top_indices = np.argsort(intensities)[-TOP_N_STARS:]
    coordinates = coordinates[top_indices]

print(f"Detected {len(coordinates)} stars in image.")

# --- Load WCS ---
hdr = fits.open(wcs_file)[0].header
wcs = WCS(hdr)

# --- Convert pixel coordinates to RA/Dec ---
world_coords = wcs.all_pix2world(coordinates, 0)
image_coords = SkyCoord(ra=world_coords[:,0]*u.deg, dec=world_coords[:,1]*u.deg)

# --- Load triangle catalog ---
tri_catalog = pd.read_csv(triangle_catalog_file)

# --- Load star catalog for HIP -> RA/Dec mapping ---
stars_df = pd.read_csv(star_catalog_file)
hip_to_coord = {row['HIP']: SkyCoord(ra=row['RArad']*u.rad, dec=row['DErad']*u.rad)
                for _, row in stars_df.iterrows()}

# --- Compute image RA/Dec limits for FOV filtering ---
nx, ny = img.shape[1], img.shape[0]
corners_pix = np.array([[0,0],[nx,0],[0,ny],[nx,ny]])
corners_world = wcs.all_pix2world(corners_pix, 0)
ra_min, ra_max = corners_world[:,0].min(), corners_world[:,0].max()
dec_min, dec_max = corners_world[:,1].min(), corners_world[:,1].max()

# --- Filter triangles that could appear in the image ---
def triangle_in_fov(row):
    try:
        coords = [hip_to_coord[row['Star1']],
                  hip_to_coord[row['Star2']],
                  hip_to_coord[row['Star3']]]
    except KeyError:
        return False
    for c in coords:
        if not (ra_min <= c.ra.deg <= ra_max and dec_min <= c.dec.deg <= dec_max):
            return False
    return True

tri_catalog = tri_catalog[tri_catalog.apply(triangle_in_fov, axis=1)]
print(f"Triangles inside FOV: {len(tri_catalog)}")

# --- Triangle voting ---
def angle(a, b):
    return a.separation(b).rad

img_triangles = []
for i, j, k in itertools.combinations(range(len(image_coords)), 3):
    s12 = angle(image_coords[i], image_coords[j])
    s13 = angle(image_coords[i], image_coords[k])
    s23 = angle(image_coords[j], image_coords[k])
    img_triangles.append({
        "i1": i, "i2": j, "i3": k,
        "Angle12": s12, "Angle13": s13, "Angle23": s23
    })

votes = {}  # pixel index -> HIP
for t in img_triangles:
    for _, row in tri_catalog.iterrows():
        if (abs(t["Angle12"] - row["Angle12"]) < ANGLE_TOL and
            abs(t["Angle13"] - row["Angle13"]) < ANGLE_TOL and
            abs(t["Angle23"] - row["Angle23"]) < ANGLE_TOL):
            for idx, hip in zip([t["i1"], t["i2"], t["i3"]],
                                [row["Star1"], row["Star2"], row["Star3"]]):
                votes[idx] = hip

# --- Print matched stars ---
if votes:
    print("\nMatched stars (after filtering):")
    for idx, hip in votes.items():
        y, x = coordinates[idx]
        print(f"Pixel ({x:.1f},{y:.1f}) -> HIP {hip}")
else:
    print("No stars matched any triangle in the catalog.")

# --- Plot image and matched stars ---
plt.figure(figsize=(10,8))
plt.imshow(img, cmap='gray', origin='lower')
plt.title("Detected Stars and Matches")

# plot all detected stars
plt.scatter(coordinates[:,1], coordinates[:,0], s=50, edgecolor='cyan', facecolor='none', label='Detected Stars')

# plot matched stars
for idx, hip in votes.items():
    y, x = coordinates[idx]
    plt.scatter(x, y, s=80, edgecolor='red', facecolor='none')
    plt.text(x+5, y+5, str(int(hip)), color='yellow', fontsize=8)

plt.legend()
plt.show()
