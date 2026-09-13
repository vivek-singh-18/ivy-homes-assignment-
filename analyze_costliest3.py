import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df_p = df[df["project_id"] == "P20165"]
print(df_p[["listing_id", "price"]])
