import json
import math
from astropy.io import fits
from astropy.wcs import WCS

# Path to your WCS FITS file
wcs_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\wcs.fits"

hdul = fits.open(wcs_file)
hdr = hdul[0].header
w = WCS(hdr)

# --- CD matrix values
CD11, CD12, CD21, CD22 = hdr["CD1_1"], hdr["CD1_2"], hdr["CD2_1"], hdr["CD2_2"]

# --- Pixel scale and rotation
scale_x = math.hypot(CD11, CD21) * 3600   # arcsec/pix
scale_y = math.hypot(CD12, CD22) * 3600
scale = (scale_x + scale_y) / 2.0
rotation = math.degrees(math.atan2(CD21, CD11))

# --- SIP coefficients (handle ndarray or dict)
def coef_dict(sip_coeff):
    d = {}
    if sip_coeff is None:
        return d
    if hasattr(sip_coeff, "shape"):  # ndarray form
        for i in range(sip_coeff.shape[0]):
            for j in range(sip_coeff.shape[1]):
                if sip_coeff[i, j] != 0:
                    d[f"{i}_{j}"] = float(sip_coeff[i, j])
    elif isinstance(sip_coeff, dict):  # dict form
        for (i, j), val in sip_coeff.items():
            d[f"{i}_{j}"] = float(val)
    return d

sip_info = {}
if w.sip is not None:
    sip = w.sip
    sip_info = {
        "a_order": int(getattr(sip, "a_order", 0)),
        "b_order": int(getattr(sip, "b_order", 0)),
        "ap_order": int(getattr(sip, "ap_order", 0)),
        "bp_order": int(getattr(sip, "bp_order", 0)),
        "a_coeffs": coef_dict(sip.a),
        "b_coeffs": coef_dict(sip.b),
        "ap_coeffs": coef_dict(getattr(sip, "ap", None)),
        "bp_coeffs": coef_dict(getattr(sip, "bp", None)),
        "crpix": [float(hdr.get("CRPIX1", 0.0)), float(hdr.get("CRPIX2", 0.0))]
    }

# --- Build final JSON
wcs_json = {
    "intrinsics": {
        "cd_matrix": {"CD1_1": CD11, "CD1_2": CD12, "CD2_1": CD21, "CD2_2": CD22},
        "pixel_scale_arcsec": scale,
        "scale_x_arcsec": scale_x,
        "scale_y_arcsec": scale_y,
        "rotation_deg": rotation,
        "sip": sip_info
    },
    "extrinsics": {
        "ra_center_deg": float(hdr.get("CRVAL1", 0.0)),
        "dec_center_deg": float(hdr.get("CRVAL2", 0.0)),
        "crpix": [float(hdr.get("CRPIX1", 0.0)), float(hdr.get("CRPIX2", 0.0))]
    }
}

# --- Save to JSON
out_file = "wcs_solution.json"
with open(out_file, "w") as f:
    json.dump(wcs_json, f, indent=2)

print(f"✅ WCS solution saved to {out_file}")
