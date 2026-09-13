import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["desc_norm"] = df["description"].fillna("").str.lower()

scam_phrases = [
    "token amount",
    "booking amount",
    "below market price",
    "owner moving abroad",
    "urgent sale",
    "price negotiable for a quick sale"
]

def is_fake(text):
    for p in scam_phrases:
        if p in text:
            return True
    return False

fake_df = df[df["desc_norm"].apply(is_fake)]
print("Fake listings found:", len(fake_df))
fake_ids = sorted(fake_df["listing_id"].tolist())
with open("fake_ids.json", "w") as f:
    json.dump(fake_ids, f)

