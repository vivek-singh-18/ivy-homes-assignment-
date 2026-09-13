import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)

df = pd.DataFrame(projects)
print(df[["project_id", "price_min", "price_max"]].sort_values("price_max", ascending=False).head(10).to_string())
