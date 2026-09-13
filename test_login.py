import requests
import json

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-AEC873EFB13C"
PASSWORD = "31d4e26d65"
EMAIL = "demo1@ivy.homes"

def check_login():
    print("--- POST /auth/login ---")
    r = requests.post(f"{BASE_URL}/auth/login", headers={"X-API-Key": API_KEY}, json={"email": EMAIL, "password": PASSWORD})
    print(r.status_code)
    print(r.text)

if __name__ == "__main__":
    check_login()
