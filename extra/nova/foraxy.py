from astropy.io import fits
import pandas as pd

# Path to your axy.fits file
axy_file = r"C:\Users\Test\OneDrive\Documents\Tanvi\StarTracker\nova\axy.fits"

# Open the FITS file
with fits.open(axy_file) as hdul:
    hdul.info()
    data = hdul[1].data  # the binary table

# Correct way: use data.names (list of column names)
df = pd.DataFrame({col: data[col] for col in data.names})

# Show summary in terminal
print("✅ Extracted {} detections".format(len(df)))
print("Columns:", df.columns.tolist())
print(df.head())

# Save to CSV
csv_file = "axy_detections.csv"
df.to_csv(csv_file, index=False)

# Save to JSON
json_file = "axy_detections.json"
df.to_json(json_file, orient="records", indent=2)

print(f"Saved detections to:\n- {csv_file}\n- {json_file}")
