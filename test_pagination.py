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
    
    r1 = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"page": 1, "limit": 200})
    print(r1.json().get("page"), r1.json().get("page_size"), len(r1.json().get("results")))
    
    r2 = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"page": 2, "limit": 200})
    print(r2.json().get("page"), r2.json().get("page_size"), len(r2.json().get("results")))
    
    # Are the results the same?
    res1 = r1.json().get("results")
    res2 = r2.json().get("results")
    if res1 and res2:
        print("Same results?", res1[0]["listing_id"] == res2[0]["listing_id"])
        
    r3 = requests.get(f"{BASE_URL}/v1/listings", headers=headers, params={"page": 100, "limit": 200})
    res3 = r3.json().get("results")
    print("Page 100 results:", len(res3))
