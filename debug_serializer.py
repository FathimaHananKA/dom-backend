
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from requests.serializers import DormApplicationSerializer
from requests.models import DormApplication
from allocations.models import Allocation

# Find an allocation for Mystic Mansion
alloc = Allocation.objects.filter(bed__room__dormitory__name='Mystic Mansion').first()
if not alloc:
    print("No allocations found!")
else:
    print(f"Testing with student: {alloc.student.user.username}")
    # Find application for this student
    app = DormApplication.objects.filter(student=alloc.student).first()
    if app:
        print("Found Application.")
        serializer = DormApplicationSerializer(app)
        data = serializer.data
        print(data)
        
        # Explicit check of the fields
        alloc_data = data.get('allocation', {})
        print("\n--- Allocation Data ---")
        print(f"Warden Name: {alloc_data.get('warden_name')}")
        print(f"Warden Email: {alloc_data.get('warden_email')}")
        print(f"Warden Phone: {alloc_data.get('warden_phone')}")
    else:
        print("No application found for this student.")
