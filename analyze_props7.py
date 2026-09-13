import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
# For apartments/villas, the physical characteristics should not change
dup_cols = ["apartment_name", "floor", "bedroom", "bathroom", "carpet_area", "facing_direction"]
dups = df[df.duplicated(subset=dup_cols, keep=False)]
print("Dups by strict physical characteristics:", len(dups))
if len(dups) > 0:
    print(dups[dup_cols + ["listing_id", "price", "posted_by_contact"]].sort_values(by=dup_cols).head(10).to_string())

unique_count = len(df.drop_duplicates(subset=dup_cols))
print("Unique count:", unique_count)
