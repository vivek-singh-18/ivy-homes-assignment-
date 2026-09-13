import json
import pandas as pd
from datetime import datetime, timezone, timedelta

with open("v1_listings.json") as f:
    listings = json.load(f)

with open("v1_rentals.json") as f:
    rentals = json.load(f)

with open("v1_projects.json") as f:
    projects = json.load(f)

print("1. total_listing_records")
total_listing_records = len(listings)
print(total_listing_records)

print("\n3. active_listings")
# Let's see if 'is_live' exists
if len(listings) > 0 and 'is_live' in listings[0]:
    active_listings = sum(1 for l in listings if l.get('is_live') is True)
    print("Found is_live field! count:", active_listings)
else:
    print("is_live field NOT FOUND in listings[0]!")
    if len(listings) > 0:
        print("Keys:", listings[0].keys())
