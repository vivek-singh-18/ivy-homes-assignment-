import requests
import json
import pandas as pd

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-AEC873EFB13C"
PASSWORD = "31d4e26d65"
EMAIL = "demo1@ivy.homes"

def get_token():
    r = requests.post(f"{BASE_URL}/auth/login", headers={"X-API-Key": API_KEY}, json={"email": EMAIL, "password": PASSWORD})
    r.raise_for_status()
    return r.json()["access_token"]

if __name__ == "__main__":
    token = get_token()
    headers = {"X-API-Key": API_KEY, "Authorization": f"Bearer {token}"}
    
    with open("v1_projects.json") as f:
        projects = json.load(f)
    with open("v1_listings.json") as f:
        listings = json.load(f)
        
    df_l = pd.DataFrame(listings)
    counts_all = df_l["project_id"].value_counts().to_dict()
    counts_live = df_l[df_l["is_live"] == True]["project_id"].value_counts().to_dict()
    
    for p in projects:
        pid = p["project_id"]
        claimed = p["total_listings"]
        actual_all = counts_all.get(pid, 0)
        actual_live = counts_live.get(pid, 0)
        if claimed != actual_live and claimed != actual_all:
            print(f"Project {pid}: claimed {claimed}, actual_live {actual_live}, actual_all {actual_all}")
            r = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"project_id": pid})
            print(f"API total for project_id {pid}: {r.json().get('total')}")
            break
