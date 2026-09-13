import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
# Clean description
df["desc_norm"] = df["description"].str.strip().str.lower()
dup_desc = df[df.duplicated(subset=["desc_norm"], keep=False)]
print("Dups by description:", len(dup_desc))
if len(dup_desc) > 0:
    print(dup_desc[["listing_id", "desc_norm", "price", "apartment_name"]].sort_values("desc_norm").head(10).to_string())

