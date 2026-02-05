
import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.conf import settings
import razorpay

def test_keys():
    print(f"Testing Keys from settings.py")
    print(f"Key ID: {settings.RAZORPAY_KEY_ID}")
    print(f"Key Secret: {'*' * len(settings.RAZORPAY_KEY_SECRET) if settings.RAZORPAY_KEY_SECRET else 'None'}")

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Try to fetch current orders (or create one) to test auth
        print("Attempting to create a test order...")
        data = {
            'amount': 100, # 1 rupee
            'currency': 'INR',
            'receipt': 'test_receipt',
            'payment_capture': 1
        }
        order = client.order.create(data=data)
        print("SUCCESS! Keys are valid.")
        print(f"Created Order ID: {order['id']}")
        
    except Exception as e:
        print("FAILURE! Keys appear invalid or something else is wrong.")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_keys()
