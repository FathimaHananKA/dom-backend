import requests
import json

BASE_URL = 'http://localhost:8000/api'

def verify_student_fetch():
    # 1. Login
    login_url = f'{BASE_URL}/auth/login/'
    creds = {
        'username': 'hanan@gmail.com',
        'password': '987654321'
    }
    
    print(f"Logging in with {creds['username']}...")
    try:
        response = requests.post(login_url, json=creds)
        if response.status_code != 200:
            print(f"Login Failed: {response.text}")
            return
        
        token = response.json()['access']
        print("Login Successful. Token obtained.")
        
        # 2. Fetch Students
        students_url = f'{BASE_URL}/student-profiles/'
        headers = {'Authorization': f'Bearer {token}'}
        
        print("Fetching student profiles...")
        response = requests.get(students_url, headers=headers)
        
        if response.status_code == 200:
            students = response.json()
            print(f"Success! Found {len(students)} students.")
            print(json.dumps(students, indent=2))
        else:
            print(f"Failed to fetch students. Status: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_student_fetch()
