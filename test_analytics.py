import requests

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
    
    paths = [
        "/v1/analytics/summary",
        "/v1/analytics",
        "/analytics/summary",
        "/v1/summary",
        "/summary"
    ]
    for p in paths:
        r = requests.get(f"{BASE_URL}{p}", headers=headers)
        print(f"{p}: {r.status_code}")
        if r.status_code == 200:
            print(r.text[:200])
