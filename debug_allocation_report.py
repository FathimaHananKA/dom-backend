import os
import django

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from reports.views import AllocationReport
from django.contrib.auth.models import AnonymousUser
from allocations.models import Allocation

def test_allocation_report():
    print("Testing AllocationReport view logic...")
    factory = APIRequestFactory()
    request = factory.get('/api/reports/allocations/')
    request.user = AnonymousUser() 
    
    view = AllocationReport.as_view()
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        data = response.data
        
        # Find Athira
        athira_data = next((item for item in data if item['student'] == 'Athira'), None)
        
        if athira_data:
            print("Data for Athira:")
            print(athira_data)
        else:
            print("Athira not found in report data.")
    except Exception as e:
        print(f"View execution failed: {e}")

if __name__ == "__main__":
    test_allocation_report()
