import pandas as pd
import numpy as np
from itertools import combinations

# ----------------------------
# File paths
# ----------------------------
catalog_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\filtered_stars_38.csv"
output_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\catalog_triangles_limited_50.csv"

# ----------------------------
# Load catalog and sort by brightness
# ----------------------------
catalog = pd.read_csv(catalog_file)
catalog_sorted = catalog.sort_values('Hpmag')  # smallest magnitude = brightest

# Choose top N brightest stars (adjustable)
N_brightest = 50
catalog_top = catalog_sorted.head(N_brightest)
print(f"Using top {N_brightest} brightest stars for triangle generation.")

# ----------------------------
# Reference RA/Dec for tangent-plane conversion
# ----------------------------
ra0 = catalog_top['RArad'].mean()
dec0 = catalog_top['DErad'].mean()

# Convert RA/Dec to tangent-plane coordinates
cat_x = (catalog_top['RArad'].values - ra0) * np.cos(np.radians(dec0))
cat_y = catalog_top['DErad'].values - dec0
catalog_plane = np.column_stack((cat_x, cat_y))

# ----------------------------
# Generate triangle features
# ----------------------------
triangles = list(combinations(range(len(catalog_plane)), 3))
triangle_features = []

for tri in triangles:
    a, b, c = catalog_plane[list(tri)]
    d1 = np.linalg.norm(b - a)
    d2 = np.linalg.norm(c - b)
    d3 = np.linalg.norm(a - c)
    sides = sorted([d1, d2, d3])
    triangle_features.append({
        'i1': tri[0],
        'i2': tri[1],
        'i3': tri[2],
        'r1': sides[0]/sides[2],  # shortest / longest
        'r2': sides[1]/sides[2]   # middle / longest
    })

print(f"Generated {len(triangle_features)} triangle features.")

# ----------------------------
# Save to CSV
# ----------------------------
df_triangles = pd.DataFrame(triangle_features)
df_triangles.to_csv(output_file, index=False)
print(f"Triangle features saved to: {output_file}")
