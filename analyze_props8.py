import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
dup_cols = ['apartment_name', 'floor', 'bedroom', 'bathroom']
dups = df[df.duplicated(subset=dup_cols, keep=False)]
print(len(dups))

# Group by apartment, floor, bed, bath, facing_direction
dup_cols2 = ['apartment_name', 'floor', 'bedroom', 'bathroom', 'facing_direction']
dups2 = df[df.duplicated(subset=dup_cols2, keep=False)]
print(len(dups2))

# What if we just round the coordinates to 4 decimals?
df["lat_round"] = df["latitude"].round(4)
df["lon_round"] = df["longitude"].round(4)
dup_coords = df[df.duplicated(subset=["lat_round", "lon_round", "floor"], keep=False)]
print("Dups by coords + floor:", len(dup_coords))
