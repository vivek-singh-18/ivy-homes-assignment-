import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["price_per_sqft"] = df["price"] / df["carpet_area"]

# low price per sqft < 4000
low_price = df[df["price_per_sqft"] < 4500]
print("Low price listings count:", len(low_price))
for d in low_price["description"].head(20):
    print("---", d)
