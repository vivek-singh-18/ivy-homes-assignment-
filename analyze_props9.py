import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)

def get_area_sqft(row):
    if row["listing_id"].startswith("MAG-"):
        return round(row["carpet_area"] * 10.7639104)
    return row["carpet_area"]

df["area_sqft"] = df.apply(get_area_sqft, axis=1)

# Are there duplicates based on project_id, floor, bedroom, area_sqft?
dup_cols = ["project_id", "floor", "bedroom", "area_sqft"]
dups = df[df.duplicated(subset=dup_cols, keep=False)]
print("Dups by strict normalized area:", len(dups))
unique_count = len(df.drop_duplicates(subset=dup_cols))
print("Unique properties:", unique_count)
