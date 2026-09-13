import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)
with open("v1_listings.json") as f:
    listings = json.load(f)

df_l = pd.DataFrame(listings)
counts_live = df_l[df_l["is_live"] == True]["project_id"].value_counts().to_dict()

wrong = []
for p in projects:
    pid = p["project_id"]
    claimed = p["total_listings"]
    actual = counts_live.get(pid, 0)
    if claimed != actual:
        wrong.append((pid, claimed, actual))

wrong.sort(key=lambda x: abs(x[1]-x[2]), reverse=True)
print("Top discrepancies (pid, claimed, actual):")
for w in wrong[:20]:
    print(w)
