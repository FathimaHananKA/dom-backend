"""
Test script to verify dormitory room and bed counts are calculated correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from dormitories.models import Dormitory
from dormitories.serializers import DormitorySerializer
from rooms.models import Room, Bed

print("=" * 60)
print("DORMITORY ROOM AND BED COUNT VERIFICATION")
print("=" * 60)

dormitories = Dormitory.objects.all()

for dorm in dormitories:
    # Get actual counts from database
    actual_rooms = Room.objects.filter(dormitory=dorm).count()
    actual_beds = Bed.objects.filter(room__dormitory=dorm).count()
    
    # Get serialized data
    serializer = DormitorySerializer(dorm)
    serialized_data = serializer.data
    
    print(f"\n{dorm.name} ({dorm.gender}):")
    print(f"  Stored in DB - Rooms: {dorm.total_rooms}, Beds: {dorm.total_beds}")
    print(f"  Actual Count - Rooms: {actual_rooms}, Beds: {actual_beds}")
    print(f"  Serialized   - Rooms: {serialized_data['total_rooms']}, Beds: {serialized_data['total_beds']}")
    
    if actual_rooms == serialized_data['total_rooms'] and actual_beds == serialized_data['total_beds']:
        print(f"  ✓ Counts match correctly!")
    else:
        print(f"  ✗ Mismatch detected!")

print("\n" + "=" * 60)
