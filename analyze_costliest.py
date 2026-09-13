import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)

df = pd.DataFrame(projects)
costliest = df.loc[df["price_max"].idxmax()]
print("Q7. costliest_project:")
print(json.dumps({
    "project_id": costliest["project_id"],
    "price_max_inr": int(costliest["price_max"])
}, indent=2))
