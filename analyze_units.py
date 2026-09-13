import json
import pandas as pd
import numpy as np

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
# Extract website prefix from listing_id
df["prefix"] = df["listing_id"].str[:3]

print(df.groupby("prefix")["carpet_area"].describe())
