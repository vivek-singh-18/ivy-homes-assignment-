import json

with open("v1_listings.json") as f:
    listings = json.load(f)

print("Total elements in list:", len(listings))

ids = [l["listing_id"] for l in listings]
print("Unique listing_ids:", len(set(ids)))

# Check if there are duplicates
import collections
counts = collections.Counter(ids)
dups = {k: v for k, v in counts.items() if v > 1}
print("Duplicate IDs count:", len(dups))
if dups:
    print("Example duplicate ID:", list(dups.keys())[0])
