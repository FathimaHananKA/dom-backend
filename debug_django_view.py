
import os
import sys
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from allocations.models import Allocation
from payments.models import Payment
from payments.views import CreateOrderView
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

User = get_user_model()

print("1. Finding a Student User with Allocation...")
try:
    # Find a user who has an allocation
    # We loop through allocations to get a valid student user
    allocation = Allocation.objects.first()
    if not allocation:
        print("   [ERROR] No allocations found in database. Cannot test payment.")
        sys.exit(1)
        
    student_profile = allocation.student
    user = student_profile.user
    print(f"   [SUCCESS] Found User: {user.username} (ID: {user.id})")
    print(f"   Student Profile: {student_profile}")
    print(f"   Allocation: {allocation}")

    print("\n2. Simulating View Execution...")
    try:
        # Mocking a Request
        factory = APIRequestFactory()
        request = factory.post('/api/payments/create-order/', {}, format='json')
        request.user = user
        
        # Instantiate View
        view = CreateOrderView()
        
        # Manually triggering the logic inside post (or calling view)
        # We'll just run the method directly to catch exceptions
        response = view.post(request)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Data: {response.data}")
        
        if response.status_code == 200 or response.status_code == 201:
             print("   [SUCCESS] View executed successfully.")
        else:
             print("   [FAILURE] View returned error status.")

    except Exception as e:
        print("   [EXCEPTION] Exception during view execution:")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"   [ERROR] Setup failed: {e}")
