import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
# A single physical property would be in the same project, on the same floor, with the same bedroom, 
# and likely posted by the same contact across multiple websites?
dup_cols = ["project_id", "floor", "bedroom", "posted_by_contact"]
dups = df[df.duplicated(subset=dup_cols, keep=False)]
print("Dups by project+floor+bedroom+contact:", len(dups))

if len(dups) > 0:
    print(dups[dup_cols + ["listing_id", "carpet_area", "price", "apartment_name"]].sort_values(by=dup_cols).head(10).to_string())
