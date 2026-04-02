import numpy as np
from PIL import Image
import pandas as pd
import math

# ----------------------------
# 1. Load the BMP image
# ----------------------------
image_path = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\bmp_4.bmp"
img = Image.open(image_path)
img_array = np.array(img)
height, width = img_array.shape[:2]

# ----------------------------
# 2. WCS parameters
# ----------------------------
# Reference pixel
CRPIX1, CRPIX2 = 100.150993347, 292.488810221

# RA/Dec center
RA_center = 100.593422824  # deg
Dec_center = 14.1734472004 # deg

# CD matrix (degrees/pixel)
CD1_1 = 0.00247980763309
CD1_2 = -0.0198359470851
CD2_1 = 0.0197560563967
CD2_2 = 0.00254454029158

# SIP forward distortion coefficients
a = {(0,2): 1.73511739026e-05, (1,1): -6.16988535672e-06, (2,0): 2.57133139154e-05}
b = {(0,2): 3.01605829417e-05, (1,1): 2.76894595917e-05, (2,0): -1.64756754909e-06}

# ----------------------------
# 3. Create pixel grid
# ----------------------------
y_pix, x_pix = np.indices((height, width))
dx = x_pix - CRPIX1
dy = y_pix - CRPIX2

# ----------------------------
# 4. Apply CD matrix in arcseconds
# ----------------------------
# Convert CD from degrees → arcseconds
CD1_1_arcsec = CD1_1 * 3600
CD1_2_arcsec = CD1_2 * 3600
CD2_1_arcsec = CD2_1 * 3600
CD2_2_arcsec = CD2_2 * 3600

u = CD1_1_arcsec * dx + CD1_2_arcsec * dy
v = CD2_1_arcsec * dx + CD2_2_arcsec * dy

# ----------------------------
# 5. Apply SIP distortion
# ----------------------------
u_sip = u + a.get((2,0),0)*dx**2 + a.get((1,1),0)*dx*dy + a.get((0,2),0)*dy**2
v_sip = v + b.get((2,0),0)*dx**2 + b.get((1,1),0)*dx*dy + b.get((0,2),0)*dy**2

# ----------------------------
# 6. Convert arcseconds → degrees
# ----------------------------
u_deg = u_sip / 3600.0
v_deg = v_sip / 3600.0

# ----------------------------
# 7. Compute RA/Dec (tangent plane projection)
# ----------------------------
RA = RA_center + u_deg / np.cos(np.radians(Dec_center))
Dec = Dec_center + v_deg

# ----------------------------
# 8. Save RA/Dec to CSV
# ----------------------------
# Flatten arrays for CSV
df = pd.DataFrame({
    'x_pix': x_pix.flatten(),
    'y_pix': y_pix.flatten(),
    'RA_deg': RA.flatten(),
    'Dec_deg': Dec.flatten()
})

# Increase float precision in CSV
pd.options.display.float_format = '{:.12f}'.format

output_csv = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\bmp_4_RA_Dec.csv"
df.to_csv(output_csv, index=False)

print(f"RA/Dec coordinates saved to {output_csv}")
