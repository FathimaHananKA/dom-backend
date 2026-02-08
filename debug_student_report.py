import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from reports.views import StudentReport
from django.contrib.auth import get_user_model

User = get_user_model()

def test_student_report():
    print("Testing StudentReport view logic with Admin user...")
    factory = APIRequestFactory()
    request = factory.get('/api/reports/students/')
    
    # Get Admin User
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("No admin user found to test with.")
        return

    force_authenticate(request, user=admin_user)
    
    view = StudentReport.as_view()
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        data = response.data
        
        if isinstance(data, list):
             # Find Athira
            athira_data = next((item for item in data if item['username'] == 'Athira'), None)
            
            if athira_data:
                print("Data for Athira:")
                print(athira_data)
                if athira_data.get('payment_status') == 'Paid':
                    print("✅ Payment Status is PAID")
                else:
                    print(f"❌ Payment Status is {athira_data.get('payment_status')}")
            else:
                print("Athira not found in report data.")
        else:
            print(f"Response data is not a list: {data}")

    except Exception as e:
        print(f"View execution failed: {e}")

if __name__ == "__main__":
    test_student_report()
