import requests
import json
import os

BASE_URL = 'http://localhost:8000/api'

def verify_wardens():
    # Attempt login to get token
    login_url = f'{BASE_URL}/auth/login/'
    
    # Using credentials seen in debug_login.py, assuming they are valid admin
    payload = {
        'username': 'hanan@gmail.com',
        'password': '987654321'
    }
    
    print(f"Logging in with {payload['username']}...")
    try:
        r = requests.post(login_url, json=payload)
        print(f"Login Status: {r.status_code}")
        if r.status_code == 200:
            tokens = r.json()
            access_token = tokens.get('access')
            print("Login successful, got token.")
        else:
            print(f"Login failed: {r.text}")
            access_token = None
    except Exception as e:
        print(f"Login Exception: {e}")
        access_token = None

    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    # Check /api/wardens/
    wardens_url = f'{BASE_URL}/wardens/'
    print(f"\nChecking {wardens_url}...")
    try:
        r = requests.get(wardens_url, headers=headers)
        print(f"Status: {r.status_code}")
        # print(f"Response: {r.text[:200]}") # Truncate 
    except Exception as e:
        print(f"Error checking wardens: {e}")

    # Check /api/warden-profiles/
    warden_profiles_url = f'{BASE_URL}/warden-profiles/'
    print(f"\nChecking {warden_profiles_url}...")
    try:
        r = requests.get(warden_profiles_url, headers=headers)
        print(f"Status: {r.status_code}")
        # print(f"Response: {r.text[:200]}")
    except Exception as e:
        print(f"Error checking warden-profiles: {e}")

if __name__ == '__main__':
    verify_wardens()
