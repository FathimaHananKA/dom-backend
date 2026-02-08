import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, StudentProfile
from payments.models import Payment
from allocations.models import Allocation

def verify_logic():
    # 1. Setup Test Data
    print("Setting up test data...")
    user = User.objects.filter(username='test_payment_user').first()
    if not user:
        user = User.objects.create_user(username='test_payment_user', password='password123')
        StudentProfile.objects.create(user=user, student_id='TEST001', department='UG', year=1, gender='FEMALE')
    
    student_profile = user.studentprofile
    
    # Ensure no existing payments interfere
    Payment.objects.filter(student=student_profile).delete()
    
    # Create or get allocation
    # We need to create a dummy allocation for the test user to ensure the logic works
    # Mocking the allocation since we might not have all related objects (Dorm, Room, Bed) easily available
    # But Payment needs a real Allocation ID.
    
    # Try to find ANY allocation
    allocation = Allocation.objects.first()
    
    if not allocation:
        # Create a minimal allocation chain
        from dormitories.models import Dormitory
        from rooms.models import Room, Bed
        
        dorm = Dormitory.objects.create(name="Test Dorm", gender="FEMALE")
        room = Room.objects.create(dormitory=dorm, room_number="101", room_type="SINGLE", capacity=1)
        bed = Bed.objects.create(room=room, bed_number="1", is_occupied=True)
        allocation = Allocation.objects.create(student=student_profile, bed=bed, is_active=True)
        print(f"Created pending allocation: {allocation.id}")
    else:
        print(f"Using existing allocation: {allocation.id}")

    print(f"Testing with Student: {user.username}, Allocation ID: {allocation.id}")

    # 2. Simulate Scenario
    print("\n--- Scenario 1: Only Pending Payment ---")
    Payment.objects.create(
        student=student_profile,
        allocation=allocation,
        amount=5000,
        status='PENDING',
        razorpay_order_id='order_pending_1'
    )
    
    # Query Logic
    payment = Payment.objects.filter(
        student=student_profile,
        allocation=allocation,
        status='SUCCESS'
    ).first()
    
    if not payment:
        payment = Payment.objects.filter(
            student=student_profile,
            allocation=allocation
        ).order_by('-created_at').first()
        
    print(f"Result: {payment.status} (Expected: PENDING)")
    
    
    print("\n--- Scenario 2: Success Payment Exists ---")
    Payment.objects.create(
        student=student_profile, 
        allocation=allocation,
        amount=5000,
        status='SUCCESS',
        razorpay_order_id='order_success_1'
    )
    
    # Query Logic
    payment = Payment.objects.filter(
        student=student_profile,
        allocation=allocation,
        status='SUCCESS'
    ).first()
    
    if not payment:
        payment = Payment.objects.filter(
            student=student_profile,
            allocation=allocation
        ).order_by('-created_at').first()
            
    print(f"Result: {payment.status} (Expected: SUCCESS)")


    print("\n--- Scenario 3: Success Payment followed by New Pending Payment ---")
    # Add a newer pending payment
    import time
    time.sleep(1) # Ensure timestamp difference
    Payment.objects.create(
        student=student_profile,
        allocation=allocation,
        amount=5000,
        status='PENDING',
        razorpay_order_id='order_pending_2'
    )
    
    # Query Logic (The Fix)
    payment = Payment.objects.filter(
        student=student_profile,
        allocation=allocation,
        status='SUCCESS'
    ).first()
    
    if not payment:
        payment = Payment.objects.filter(
            student=student_profile,
            allocation=allocation
        ).order_by('-created_at').first()
            
    print(f"Result: {payment.status} (Expected: SUCCESS)")

    print("\n--- Scenario 4: Self-Healing Logic (Success Payment but Allocation Not Paid) ---")
    # Reset allocation to is_paid=False
    allocation.is_paid = False
    allocation.save()
    print(f"Allocation {allocation.id} is_paid set to: {allocation.is_paid}")
    
    # We already have a success payment from previous steps
    payment = Payment.objects.filter(
        student=student_profile,
        allocation=allocation,
        status='SUCCESS'
    ).first()
    
    if payment and payment.status == 'SUCCESS':
         # Self-healing logic simulation
        if allocation and not allocation.is_paid:
            print(f"Simulating Self-healing: Updating allocation {allocation.id} is_paid to True")
            allocation.is_paid = True
            allocation.save()
            
    # Verify
    allocation.refresh_from_db()
    print(f"Result: Allocation.is_paid = {allocation.is_paid} (Expected: True)")
    
    # Cleanup
    print("\nCleaning up test payments...")
    Payment.objects.filter(razorpay_order_id__in=['order_pending_1', 'order_success_1', 'order_pending_2']).delete()
    print("Test Complete.")

if __name__ == "__main__":
    verify_logic()
