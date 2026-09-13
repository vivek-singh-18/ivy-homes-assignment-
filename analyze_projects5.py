import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)
with open("v1_listings.json") as f:
    listings = json.load(f)
with open("v1_rentals.json") as f:
    rentals = json.load(f)

df_l = pd.DataFrame(listings)
df_r = pd.DataFrame(rentals)

# Do rentals have project_id?
print("Rentals columns:", df_r.columns)
if 'project_id' in df_r.columns:
    counts_rentals = df_r["project_id"].value_counts().to_dict()
else:
    counts_rentals = {}

counts_live = df_l[df_l["is_live"] == True]["project_id"].value_counts().to_dict()

wrong = []
for p in projects:
    pid = p["project_id"]
    claimed = p["total_listings"]
    actual = counts_live.get(pid, 0) + counts_rentals.get(pid, 0)
    if claimed != actual:
        wrong.append((pid, claimed, actual))

print(f"Wrong if live + rentals: {len(wrong)}")
