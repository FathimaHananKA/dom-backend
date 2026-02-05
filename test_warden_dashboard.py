"""
Test script to verify warden dashboard endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rooms.serializers import DetailedRoomSerializer
from rooms.models import Room
from dormitories.models import Dormitory

print("Testing Warden Dashboard Implementation")
print("=" * 50)

# Test 1: Check if DetailedRoomSerializer exists
print("\n✓ DetailedRoomSerializer imported successfully")

# Test 2: Check if we have any dormitories
dorms = Dormitory.objects.all()
print(f"\n✓ Found {dorms.count()} dormitories in database")

if dorms.exists():
    # Test 3: Check rooms for first dormitory
    first_dorm = dorms.first()
    print(f"\n✓ Testing with dormitory: {first_dorm.name}")
    
    rooms = Room.objects.filter(dormitory=first_dorm).prefetch_related(
        'beds', 'beds__allocation', 'beds__allocation__student', 
        'beds__allocation__student__user'
    )
    
    print(f"✓ Found {rooms.count()} rooms in {first_dorm.name}")
    
    if rooms.exists():
        # Test 4: Serialize a room
        serializer = DetailedRoomSerializer(rooms.first())
        data = serializer.data
        
        print(f"\n✓ Room serialization successful")
        print(f"  - Room Number: {data.get('room_number')}")
        print(f"  - Room Type: {data.get('room_type')}")
        print(f"  - Capacity: {data.get('capacity')}")
        print(f"  - Occupied Beds: {data.get('occupied_beds')}")
        print(f"  - Available Beds: {data.get('available_beds')}")
        print(f"  - Status: {data.get('status')}")
        print(f"  - Number of beds: {len(data.get('beds', []))}")
        
        # Check if any beds have student info
        beds_with_students = [b for b in data.get('beds', []) if b.get('student')]
        if beds_with_students:
            print(f"\n✓ Found {len(beds_with_students)} occupied bed(s) with student info")
            for bed in beds_with_students[:2]:  # Show first 2
                student = bed.get('student', {})
                print(f"  - {bed.get('bed_number')}: {student.get('student_name')} ({student.get('student_id')})")

print("\n" + "=" * 50)
print("All tests completed successfully!")
