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
    
    r1 = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"offset": 0, "limit": 200})
    print("Offset 0:", len(r1.json().get("results")))
    
    r2 = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"offset": 50, "limit": 200})
    print("Offset 50:", len(r2.json().get("results")))
    
    res1 = r1.json().get("results")
    res2 = r2.json().get("results")
    if res1 and res2:
        print("Same results?", res1[0]["listing_id"] == res2[0]["listing_id"])
