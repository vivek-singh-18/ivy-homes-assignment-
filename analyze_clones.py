import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)

# Normalize string fields to group them
df["apt"] = df["apartment_name"].str.lower().str.replace(r'[^a-z]', '', regex=True)

# Group by apartment, floor, bedroom
groups = df.groupby(["apt", "floor", "bedroom"])

# Check if prices are identical or very close? Or if areas are same?
def get_area_sqft(row):
    if row["listing_id"].startswith("MAG-"):
        return round(row["carpet_area"] * 10.7639104)
    return row["carpet_area"]

df["area_sqft"] = df.apply(get_area_sqft, axis=1)

dup_cols = ["apt", "floor", "bedroom", "area_sqft", "facing_direction"]
print("Unique properties (apt, floor, bed, area, facing):", len(df.drop_duplicates(subset=dup_cols)))

