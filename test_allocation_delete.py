"""
Test script to verify allocation deletion properly updates bed status
Creates test data if needed
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from allocations.models import Allocation
from rooms.models import Bed, Room
from accounts.models import StudentProfile, User
from dormitories.models import Dormitory

print("=" * 60)
print("ALLOCATION DELETION SIGNAL TEST")
print("=" * 60)

# Try to find existing allocation
existing_alloc = Allocation.objects.first()

if existing_alloc:
    print("\n✓ Found existing allocation to test with")
    bed = existing_alloc.bed
    student = existing_alloc.student
    
    print(f"\nAllocation: {existing_alloc}")
    print(f"  Bed: {bed.bed_number}")
    print(f"  Student: {student.user.username if student.user else 'Unknown'}")
    print(f"  Bed Status BEFORE delete: {'Occupied' if bed.is_occupied else 'Available'}")
    
    # Store IDs for recreation
    bed_id = bed.id
    student_id = student.id
    
    # Delete the allocation
    existing_alloc.delete()
    
    # Refresh the bed from database
    bed.refresh_from_db()
    
    print(f"  Bed Status AFTER delete: {'Occupied' if bed.is_occupied else 'Available'}")
    
    if not bed.is_occupied:
        print(f"\n✅ SUCCESS: Signal is working! Bed correctly marked as available!")
    else:
        print(f"\n❌ FAILED: Signal not working. Bed still marked as occupied!")
    
    # Recreate the allocation
    try:
        new_alloc = Allocation.objects.create(bed=bed, student=student)
        print(f"\n✓ Allocation recreated successfully")
    except Exception as e:
        print(f"\n⚠️  Could not recreate allocation: {e}")
        
else:
    print("\n⚠️  No existing allocations found")
    print("Creating test data...")
    
    # Find or create test resources
    room = Room.objects.filter(beds__isnull=False).first()
    if not room:
        print("❌ No rooms with beds found. Cannot create test allocation.")
    else:
        bed = room.beds.filter(is_occupied=False).first()
        if not bed:
            bed = room.beds.first()
            
        student = StudentProfile.objects.first()
        
        if not student:
            print("❌ No students found. Cannot create test allocation.")
        else:
            print(f"\nCreating test allocation:")
            print(f"  Bed: {bed.bed_number}")
            print(f"  Student: {student.user.username if student.user else 'Unknown'}")
            
            # Create allocation
            try:
                alloc = Allocation.objects.create(bed=bed, student=student)
                bed.refresh_from_db()
                print(f"  Bed Status AFTER create: {'Occupied' if bed.is_occupied else 'Available'}")
                
                # Now delete it
                print(f"\nDeleting allocation...")
                alloc.delete()
                bed.refresh_from_db()
                print(f"  Bed Status AFTER delete: {'Occupied' if bed.is_occupied else 'Available'}")
                
                if not bed.is_occupied:
                    print(f"\n✅ SUCCESS: Signal is working! Bed correctly marked as available!")
                else:
                    print(f"\n❌ FAILED: Signal not working. Bed still marked as occupied!")
                    
            except Exception as e:
                print(f"❌ Error creating/deleting allocation: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
