import requests
import json

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
    r = requests.get(f"{BASE_URL}/v1/analytics/summary", headers={"X-API-Key": API_KEY, "Authorization": f"Bearer {token}"})
    print(r.status_code)
    with open("v1_analytics_summary.json", "w") as f:
        json.dump(r.json(), f, indent=2)
