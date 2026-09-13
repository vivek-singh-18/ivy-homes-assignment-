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
    
    filters = [
        {"locality": "kukatpally"},
        {"bhk": 3},
        {"property_type": "villa"},
        {"min_price": 20000000},
        {"max_price": 5000000},
        {"furnishing": "fully-furnished"},
        {"project_id": "P20001"}
    ]
    
    print("Testing /v1/listings filters:")
    for f in filters:
        r = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params=f)
        total = r.json().get("total")
        print(f"Filter {f}: total = {total}")

    print("\nTesting /v1/rentals filters:")
    for f in filters:
        if "project_id" in f: continue
        r = requests.get(f"{BASE_URL}/v1/rentals", headers=headers, params=f)
        total = r.json().get("total")
        print(f"Filter {f}: total = {total}")
