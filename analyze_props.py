import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
# Let's find duplicates based on some fields
# Same property might have same latitude, longitude, floor, bhk, property_type
dup_cols = ["latitude", "longitude", "floor", "bedroom", "property_type"]
duplicates = df[df.duplicated(subset=dup_cols, keep=False)]
print("Number of records sharing physical location attributes:", len(duplicates))

# Group by the dup_cols to see how many unique properties there are
unique_props = df.drop_duplicates(subset=dup_cols)
print("Unique physical properties based on strict matching:", len(unique_props))

# Wait, what if coordinates have slight jitter? 
# Maybe just project_id + floor + bedroom + carpet_area ?
dup_cols2 = ["project_id", "floor", "bedroom", "carpet_area"]
# drop rows where project_id is null for this test
df_proj = df.dropna(subset=["project_id"])
dup_proj = df_proj[df_proj.duplicated(subset=dup_cols2, keep=False)]
print("Duplicates based on project_id+floor+bedroom+area:", len(dup_proj))

# Let's look at a few examples of "duplicate" listings
if len(duplicates) > 0:
    print(duplicates[dup_cols + ["listing_id", "price", "posted_by", "project_id", "apartment_name"]].sort_values(by=dup_cols).head(10).to_string())
