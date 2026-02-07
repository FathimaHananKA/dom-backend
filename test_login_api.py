import requests
import json

def test_login(username, password):
    url = "http://127.0.0.1:8000/api/auth/login/"
    data = {
        "username": username,
        "password": password
    }
    print(f"Testing login for {username}...")
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login("admin", "987654321")
