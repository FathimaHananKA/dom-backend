import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/auth/login/"

def test_login(username, password, description):
    print(f"\n--- Testing: {description} ---")
    data = {
        "username": username,
        "password": password
    }
    jsondata = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE_URL, data=jsondata, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            print(f"Status Code: {status_code}")
            # print(f"Response: {response_body}") 
            print("✅ Login SUCCESS")
            
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        print(f"Response Error: {e.read().decode('utf-8')}")
        if e.code == 400:
            print("❌ Login FAILED (Expected 400 for bad creds)")
        else:
            print(f"⚠️ Unexpected Status: {e.code}")
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    # 1. Valid Admin Login (Should Succeed)
    test_login("admin", "987654321", "Valid Admin (987654321)")
    
    # 2. Valid Student Login (Athira)
    test_login("Athira", "987654321", "Valid Student (Athira)")
