import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from reports.views import AllocationReport
from django.contrib.auth import get_user_model

User = get_user_model()

def test_allocation_report():
    print("Testing AllocationReport view logic with Admin user...")
    factory = APIRequestFactory()
    request = factory.get('/api/reports/allocations/')
    
    # Get Admin User
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("No admin user found to test with.")
        return

    force_authenticate(request, user=admin_user)
    
    view = AllocationReport.as_view()
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        data = response.data
        
        if isinstance(data, list):
             # Find Athira
            athira_data = next((item for item in data if item['student'] == 'Athira'), None)
            
            if athira_data:
                print("Data for Athira:")
                print(athira_data)
            else:
                print("Athira not found in report data.")
        else:
            print(f"Response data is not a list: {data}")

    except Exception as e:
        print(f"View execution failed: {e}")

if __name__ == "__main__":
    test_allocation_report()
