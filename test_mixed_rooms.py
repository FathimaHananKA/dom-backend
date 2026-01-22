import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dombackend.settings")
django.setup()

from dormitories.serializers import DormitorySerializer
from dormitories.models import Dormitory
from rooms.models import Room

# Cleanup previous test
Dormitory.objects.filter(name="Mixed Dorm Test").delete()

data = {
    "name": "Mixed Dorm Test",
    "gender": "Male",
    "room_configurations": [
        {"prefix": "A", "count": 3, "type": "single"}, # A1-A3, cap=1. Total beds=3
        {"prefix": "B", "count": 2, "type": "double"}, # B1-B2, cap=2. Total beds=4
    ]
}

serializer = DormitorySerializer(data=data)
if serializer.is_valid():
    dorm = serializer.save()
    print(f"Dorm Created: {dorm.name}")
    print(f"Total Rooms: {dorm.total_rooms} (Expected 5)")
    print(f"Total Beds: {dorm.total_beds} (Expected 7)")
    
    rooms = Room.objects.filter(dormitory=dorm).order_by('room_number')
    for r in rooms:
        print(f"Room: {r.room_number}, Type: {r.room_type}, Cap: {r.capacity}")
        
    expected_rooms = ["A1", "A2", "A3", "B1", "B2"]
    actual_rooms = [r.room_number for r in rooms]
    
    if actual_rooms == expected_rooms and dorm.total_rooms == 5 and dorm.total_beds == 7:
        print("SUCCESS: Mixed room creation verified.")
    else:
        print("FAILURE: Data mismatch.")
else:
    print(serializer.errors)
