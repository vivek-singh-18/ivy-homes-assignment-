import json
import pandas as pd
import re

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["desc_norm"] = df["description"].fillna("").str.lower()

scam_phrases = [
    "pay a token amount of rs 25,000 today to block the unit",
    "site visit only after the booking amount is paid",
    "below market price, this week only"
]

def is_fake(text):
    for p in scam_phrases:
        if p in text:
            return True
    return False

fake_df = df[df["desc_norm"].apply(is_fake)]
print("Fake listings found:", len(fake_df))

fake_ids = sorted(fake_df["listing_id"].tolist())
print(fake_ids[:10])

# Just to be sure, check if there are other suspicious phrases.
# e.g., "owner moving abroad, priced to sell", "urgent sale - owner relocating"
# let's see if all fake ones have one of these 3 phrases.
# If so, fake_ids is our answer for Q9.
with open("fake_ids.txt", "w") as f:
    for fid in fake_ids:
        f.write(f"{fid}\n")

