import json
import pandas as pd

with open("v1_projects.json") as f:
    projects = json.load(f)
with open("v1_listings.json") as f:
    listings = json.load(f)

# Count listings per project
df_l = pd.DataFrame(listings)
# Only count live? Or all? API says: "always agrees with what GET /v1/listings?project_id=... returns"
# Let's count all listings for each project
counts = df_l["project_id"].value_counts().to_dict()

wrong_count = 0
for p in projects:
    pid = p["project_id"]
    claimed = p["total_listings"]
    actual = counts.get(pid, 0)
    if claimed != actual:
        wrong_count += 1
        # print(f"Project {pid}: claimed {claimed}, actual {actual}")

print(f"\n10. projects_with_wrong_listing_count: {wrong_count} out of {len(projects)}")
