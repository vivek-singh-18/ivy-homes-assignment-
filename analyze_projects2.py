import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)
with open("v1_listings.json") as f:
    listings = json.load(f)

df_l = pd.DataFrame(listings)
df_live = df_l[df_l["is_live"] == True]

counts_all = df_l["project_id"].value_counts().to_dict()
counts_live = df_live["project_id"].value_counts().to_dict()

wrong_all = 0
wrong_live = 0

for p in projects:
    pid = p["project_id"]
    claimed = p["total_listings"]
    if claimed != counts_all.get(pid, 0):
        wrong_all += 1
    if claimed != counts_live.get(pid, 0):
        wrong_live += 1

print(f"Wrong if all: {wrong_all}")
print(f"Wrong if live: {wrong_live}")
