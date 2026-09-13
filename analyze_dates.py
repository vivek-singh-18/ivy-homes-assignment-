import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)
df["posted_at"] = pd.to_datetime(df["posted_at"])

# Ensure timezone is correct. If the data is 'Z' (UTC), convert to +05:30
# "posted_at": "2026-06-14T09:20:00Z"
# But wait, what if dates are actually already in IST?
print("Sample posted_at:", df["posted_at"].head())

start_date = pd.to_datetime("2026-09-03T00:00:00+05:30")
end_date = pd.to_datetime("2026-09-10T00:00:00+05:30")

# If the data is timezone aware (UTC), we can just compare directly
last_7 = df[(df["posted_at"] >= start_date) & (df["posted_at"] < end_date)]
print("Listings last 7 days:", len(last_7))
