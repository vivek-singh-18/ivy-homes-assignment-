import requests
import json
import os

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-AEC873EFB13C"
PASSWORD = "31d4e26d65"
EMAIL = "demo1@ivy.homes"

def get_token():
    r = requests.post(f"{BASE_URL}/auth/login", headers={"X-API-Key": API_KEY}, json={"email": EMAIL, "password": PASSWORD})
    r.raise_for_status()
    return r.json()["access_token"]

def fetch_all(endpoint, token):
    headers = {
        "X-API-Key": API_KEY,
        "Authorization": f"Bearer {token}"
    }
    
    results = []
    offset = 0
    limit = 50
    
    while True:
        params = {"offset": offset, "limit": limit}
        r = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
        if r.status_code != 200:
            print(f"Failed {endpoint} at offset {offset}: {r.status_code} {r.text}")
            break
            
        data = r.json()
        new_results = data.get("results", [])
        results.extend(new_results)
        
        print(f"Fetched {len(new_results)} records at offset {offset}. Total fetched: {len(results)}/{data.get('total')}")
        
        if not data.get("has_more"):
            break
            
        offset += limit
        
    return results

if __name__ == "__main__":
    token = get_token()
    print("Got token")
    
    endpoints = ["/v1/listings", "/v1/rentals", "/v1/projects"]
    for ep in endpoints:
        print(f"Fetching {ep}...")
        data = fetch_all(ep, token)
        filename = ep.replace("/", "_")[1:] + ".json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to {filename}\n")
