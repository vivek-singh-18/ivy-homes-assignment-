import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
dup_contact = df[df.duplicated(subset=["posted_by_contact"], keep=False)]
print("Dups by contact number:", len(dup_contact))

# But agents post many properties. If posted_by == 'owner' and contact is same, might be same property?
owner_df = df[df["posted_by"] == "owner"]
dup_owner = owner_df[owner_df.duplicated(subset=["posted_by_contact"], keep=False)]
print("Dups by owner contact number:", len(dup_owner))

if len(dup_owner) > 0:
    print(dup_owner[["listing_id", "posted_by_contact", "price", "carpet_area", "floor", "apartment_name"]].sort_values("posted_by_contact").head(10).to_string())
