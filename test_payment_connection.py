
import sys

print("1. Testing Imports...")
try:
    import razorpay
    print("   [SUCCESS] razorpay imported.")
except ImportError as e:
    print(f"   [FAILURE] Could not import razorpay: {e}")
    sys.exit(1)

print("\n2. Testing API Connection...")
try:
    KEY_ID = 'rzp_test_SBxsHH8PJGL54x'
    KEY_SECRET = 'wZHtqayIs8S837GCSdT6ZvCF'
    
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    
    data = {
        'amount': 100, # 1 Rupee
        'currency': 'INR',
        'receipt': 'test_receipt_001',
        'payment_capture': 1 
    }
    
    print(f"   Attempting to create order with Key ID: {KEY_ID}")
    order = client.order.create(data=data)
    print(f"   [SUCCESS] Order Created: {order['id']}")
    print(f"   Full Order: {order}")

except Exception as e:
    print(f"   [FAILURE] API Call Failed: {e}")
    import traceback
    traceback.print_exc()
