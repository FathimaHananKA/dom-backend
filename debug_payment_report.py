import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from reports.views import PaymentReport
from django.contrib.auth import get_user_model

User = get_user_model()

def test_payment_report():
    print("Testing PaymentReport view logic with Admin user...")
    factory = APIRequestFactory()
    request = factory.get('/api/reports/payments/')
    
    # Get Admin User
    admin_user = User.objects.filter(is_superuser=True).first()
    force_authenticate(request, user=admin_user)
    
    view = PaymentReport.as_view()
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        data = response.data
        
        # Find the specific order
        target_order = "order_SDCCKUXjwetfHn"
        order_data = next((item for item in data if item['razorpay_order_id'] == target_order), None)
        
        if order_data:
            print(f"Data for Order {target_order}:")
            print(order_data)
            if order_data['status'] == 'SUCCESS':
                 print("✅ Status is SUCCESS")
            else:
                 print(f"❌ Status is {order_data['status']}")
        else:
            print(f"Order {target_order} not found in report.")

    except Exception as e:
        print(f"View execution failed: {e}")

if __name__ == "__main__":
    test_payment_report()
