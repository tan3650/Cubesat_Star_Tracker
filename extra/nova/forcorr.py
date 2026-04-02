from astropy.io import fits
import pandas as pd
import numpy as np

# Path to your corr.fits file
corr_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\corr.fits"

with fits.open(corr_file) as hdul:
    hdul.info()
    data = hdul[1].data  # table in HDU 1

# Convert each column to native-endian numpy array
cols = {}
for col in data.names:
    arr = np.array(data[col])
    if arr.dtype.byteorder not in ("=", "|"):  # if not native
        arr = arr.byteswap().view(arr.dtype.newbyteorder("="))
    cols[col] = arr

df = pd.DataFrame(cols)

print("✅ Extracted {} matched stars".format(len(df)))
print("Columns:", df.columns.tolist())
print(df.head())

# Save to CSV
csv_file = "corr_matches.csv"
df.to_csv(csv_file, index=False)

# Save to JSON
json_file = "corr_matches.json"
df.to_json(json_file, orient="records", indent=2)

print(f"Saved matches to:\n- {csv_file}\n- {json_file}")
