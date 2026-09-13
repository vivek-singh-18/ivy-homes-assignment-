import requests

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-AEC873EFB13C"

def check_health():
    print("--- /health ---")
    r = requests.get(f"{BASE_URL}/health")
    print(r.status_code)
    print(r.text)

def check_auth_query():
    print("\n--- Auth via query param ---")
    r = requests.get(f"{BASE_URL}/v1/listings?api_key={API_KEY}")
    print(r.status_code)
    print(r.text[:200])

def check_auth_header():
    print("\n--- Auth via X-API-Key header ---")
    r = requests.get(f"{BASE_URL}/v1/listings", headers={"X-API-Key": API_KEY})
    print(r.status_code)
    print(r.text[:200])
    
def check_auth_authorization_header():
    print("\n--- Auth via Authorization header ---")
    r = requests.get(f"{BASE_URL}/v1/listings", headers={"Authorization": f"Bearer {API_KEY}"})
    print(r.status_code)
    print(r.text[:200])

if __name__ == "__main__":
    check_health()
    check_auth_query()
    check_auth_header()
    check_auth_authorization_header()
