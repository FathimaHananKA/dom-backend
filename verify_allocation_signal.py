import os
import django
import sys
import shutil

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rooms.models import Room, Bed
from allocations.models import Allocation
from accounts.models import StudentProfile, User, Role

def verify_signal():
    print("Verifying Allocation Signal...")
    
    # 1. Setup: Create a temporary user, student, room, and bed
    print("Setting up test data...")
    role, _ = Role.objects.get_or_create(name='STUDENT')
    
    username = 'signal_test_user'
    if User.objects.filter(username=username).exists():
        User.objects.get(username=username).delete()
        
    user = User.objects.create_user(username=username, password='password', role=role)
    
    student = StudentProfile.objects.create(
        user=user, 
        student_id='SIGNAL123',
        department='UG',
        year=1,
        gender='MALE'
    )
    
    # Clean up previous room if exists
    Room.objects.filter(room_number='SIG-101').delete()
    
    # Create Dormitory stub if needed (assuming ID 1 exists or creating one)
    from dormitories.models import Dormitory
    dorm = Dormitory.objects.first()
    if not dorm:
        dorm = Dormitory.objects.create(name="Test Dorm", type="MENS")
        
    room = Room.objects.create(room_number='SIG-101', dormitory=dorm, capacity=1)
    bed = Bed.objects.filter(room=room).first()
    
    if not bed:
        # Should be auto-created by Room save
        print("Bed not auto-created, creating manually...")
        bed = Bed.objects.create(bed_number='SIG-101-1', room=room)
    
    # 2. Test: Create Allocation
    print("Creating Allocation...")
    allocation = Allocation.objects.create(student=student, bed=bed)
    
    # Verify bed is occupied
    bed.refresh_from_db()
    if not bed.is_occupied:
        print("FAIL: Bed should be occupied after allocation creation.")
        # Attempt manual fix to proceed with test? 
        # Actually if create() handles it, it should be true. 
        # AllocationSerializer.create handles it. Allocation.objects.create DOES NOT.
        # Wait! Models don't have save logic for side effects usually unless overridden.
        # Allocation model does NOT have save logic. Serializer does.
        # My signal is checking post_delete. 
        # So I must manually set is_occupied=True for this test setup to mimic real life.
        print("Note: Manually setting is_occupied=True (since model.create doesn't do it)...")
        bed.is_occupied = True
        bed.save()
    else:
        print("Bed occupied (likely by serializer if used, but we used model.create so this is unexpected unless model has signals).")

    # 3. Test: Delete Allocation
    print("Deleting Allocation...")
    allocation.delete()
    
    # Verify bed is available
    bed.refresh_from_db()
    
    if not bed.is_occupied:
        print("SUCCESS: Bed is marked as available after allocation deletion.")
    else:
        print("FAIL: Bed is still marked as occupied after allocation deletion.")

    # Cleanup
    print("Cleaning up...")
    room.delete()
    student.delete()
    user.delete()
    print("Cleanup complete.")

if __name__ == '__main__':
    try:
        verify_signal()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {e}")
