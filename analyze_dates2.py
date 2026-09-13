import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["posted_at"] = pd.to_datetime(df["posted_at"]) # naive

# REFERENCE = 2026-09-10T00:00:00+05:30 (IST)
# If dates in API are IST naive:
start_date = pd.to_datetime("2026-09-03T00:00:00")
end_date = pd.to_datetime("2026-09-10T00:00:00")

last_7 = df[(df["posted_at"] >= start_date) & (df["posted_at"] < end_date)]
print("Q8. listings_last_7_days:", len(last_7))

