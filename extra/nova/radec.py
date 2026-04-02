from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u

# Paths
wcs_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\wcs.fits"
image_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\new-image.fits"  # must be FITS, not BMP

# Open WCS
wcs_header = fits.getheader(wcs_file, 0)
wcs = WCS(wcs_header)

# Get image size from original image FITS
img_hdul = fits.open(image_file)
nx = img_hdul[0].header["NAXIS1"]
ny = img_hdul[0].header["NAXIS2"]

# Define corners of the image in pixel space
corners_pix = [
    [0, 0],
    [nx, 0],
    [0, ny],
    [nx, ny]
]
corners_radec = wcs.all_pix2world(corners_pix, 0)

# Convert to SkyCoord
c1 = SkyCoord(corners_radec[0][0], corners_radec[0][1], unit="deg")
c2 = SkyCoord(corners_radec[3][0], corners_radec[3][1], unit="deg")
diag_fov = c1.separation(c2)

c3 = SkyCoord(corners_radec[0][0], corners_radec[0][1], unit="deg")
c4 = SkyCoord(corners_radec[1][0], corners_radec[1][1], unit="deg")
horiz_fov = c3.separation(c4)

c5 = SkyCoord(corners_radec[0][0], corners_radec[0][1], unit="deg")
c6 = SkyCoord(corners_radec[2][0], corners_radec[2][1], unit="deg")
vert_fov = c5.separation(c6)

print(f"Horizontal FOV: {horiz_fov.to(u.deg):.2f}")
print(f"Vertical FOV:   {vert_fov.to(u.deg):.2f}")
print(f"Diagonal FOV:   {diag_fov.to(u.deg):.2f}")
