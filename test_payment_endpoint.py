import requests
import json

# Test the payment verification endpoint
url = "http://127.0.0.1:8000/api/payments/verify/"

# Test data (this will fail authentication, but should not return 404)
test_data = {
    "razorpay_order_id": "test_order",
    "razorpay_payment_id": "test_payment",
    "razorpay_signature": "test_signature"
}

try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 404:
        print("\n❌ ENDPOINT NOT FOUND (404)")
    elif response.status_code == 401 or response.status_code == 403:
        print("\n✓ ENDPOINT EXISTS (Authentication required)")
    else:
        print(f"\n✓ ENDPOINT EXISTS (Status: {response.status_code})")
        
except Exception as e:
    print(f"Error: {e}")
