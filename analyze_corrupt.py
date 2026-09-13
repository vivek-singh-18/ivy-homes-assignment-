import json
import pandas as pd

with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(listings)

corrupt = []
# 1. Floor > total_floors
c1 = df[df["floor"] > df["total_floors"]]
print("Floor > total_floors:", len(c1))
corrupt.extend(c1["listing_id"].tolist())

# 2. carpet_area > super_built_up_area
c2 = df[df["carpet_area"] > df["super_built_up_area"]]
print("carpet_area > super_built_up_area:", len(c2))
corrupt.extend(c2["listing_id"].tolist())

# 3. impossible floors (e.g. villa with 10 floors?)
c3 = df[(df["property_type"] == "villa") & (df["total_floors"] > 4)]
print("villa with >4 floors:", len(c3))
corrupt.extend(c3["listing_id"].tolist())

# 4. negative areas or price?
c4 = df[(df["carpet_area"] <= 0) | (df["price"] <= 0) | (df["super_built_up_area"] <= 0)]
print("Negative/zero area/price:", len(c4))
corrupt.extend(c4["listing_id"].tolist())

# 5. more bathrooms than reasonable?
c5 = df[df["bathroom"] > df["bedroom"] + 2]
print("Bathrooms > bedrooms + 2:", len(c5))
corrupt.extend(c5["listing_id"].tolist())

# 6. Check for duplicate IDs? (We already saw 0)
# Check for latitude/longitude out of bounds (India/Hyderabad)
c6 = df[(df["latitude"] < 17) | (df["latitude"] > 18) | (df["longitude"] < 78) | (df["longitude"] > 79)]
print("Lat/long out of Hyderabad:", len(c6))
corrupt.extend(c6["listing_id"].tolist())

# Unique corrupt IDs
corrupt = sorted(list(set(corrupt)))
print("Total corrupt IDs:", len(corrupt))
print(corrupt)
