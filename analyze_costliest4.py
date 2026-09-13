import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)
with open("v1_listings.json") as f:
    listings = json.load(f)

df = pd.DataFrame(projects)
df_l = pd.DataFrame(listings)

for _, p in df.sort_values("price_max", ascending=False).head(5).iterrows():
    pid = p["project_id"]
    p_max = p["price_max"]
    l_max = df_l[df_l["project_id"] == pid]["price"].max()
    print(f"{pid}: project price_max = {p_max}, max listing price = {l_max}")

# What if it's in LAKHS?
# 99.8 Lakhs = 99,80,000 = 9.98M
# max listing price = 23.04M!
# So the project price_max is totally different from max listing price.
