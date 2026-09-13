import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)

# Normalize apartment name
df['apt_norm'] = df['apartment_name'].str.lower().str.strip()

# Check duplicates on apt_norm, floor, bedroom
dup_cols = ["apt_norm", "floor", "bedroom"]
dups = df[df.duplicated(subset=dup_cols, keep=False)]
print("Dups by apt_norm, floor, bedroom:", len(dups))

if len(dups) > 0:
    print(dups[dup_cols + ["listing_id", "carpet_area", "price"]].sort_values(by=dup_cols).head(20).to_string())
    
