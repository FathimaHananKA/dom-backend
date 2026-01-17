import requests
import json

BASE_URL = 'http://localhost:8000/api'

def debug_login():
    url = f'{BASE_URL}/auth/login/'
    
    # Test 1: login with username
    payload = {
        'username': 'hanan@gmail.com',
        'password': '987654321'
    }
    print(f"--- Attempt 1: {payload} ---")
    try:
        r = requests.post(url, json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: login with email
    payload = {
        'email': 'hanan@gmail.com',
        'password': '987654321'
    }
    print(f"\n--- Attempt 2: {payload} ---")
    try:
        r = requests.post(url, json=payload)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    debug_login()
