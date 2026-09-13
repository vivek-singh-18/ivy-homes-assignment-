import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["id_number"] = df["listing_id"].str.split("-").str[1]
dup_ids = df[df.duplicated(subset=["id_number"], keep=False)]
print("Dups by listing_id numeric part:", len(dup_ids))

# Let's check listing_url
print("First few URLs:")
print(df["listing_url"].head())
