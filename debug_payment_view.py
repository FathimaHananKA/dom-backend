import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from payments.views import PaymentStatusView
from allocations.models import Allocation
from payments.models import Payment
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Try to get a user involved in allocation
    # Just picking the first one with a student profile
    from accounts.models import StudentProfile
    students = StudentProfile.objects.all()
    if not students.exists():
        print("No students found")
        sys.exit(0)
    
    print(f"Found {students.count()} students")

    for student_profile in students:
        user = student_profile.user
        print(f"\nTesting for user: {user.username}")
        
        # Simulate Request
        factory = APIRequestFactory()
        request = factory.get('/api/payments/status/')
        request.user = user
        
        # Instantiate view
        view = PaymentStatusView()
        
        try:
            # We can't call view.get(request) directly easily because of drf wrapping, 
            # but we can copy the logic
            
            print(f"  Getting allocation for {user.username}...")
            try:
                allocation = student_profile.allocation
                print(f"  Allocation found: {allocation.id}")
            except Exception as e:
                print(f"  No allocation: {e}")
                continue

            # Check payment
            payment = Payment.objects.filter(
                student=student_profile,
                allocation=allocation
            ).order_by('-created_at').first()
            
            if payment:
                print("  Payment exists")
            else:
                print("  No payment, trying to access details...")
                try:
                    bed = allocation.bed
                    print("  Bed accessed OK")
                    
                    if bed:
                        room = bed.room
                        print("  Room accessed OK")
                        if room:
                            dormitory = room.dormitory
                            print("  Dormitory accessed OK")
                            if dormitory:
                                warden = dormitory.warden
                                print("  Warden accessed OK")
                except Exception as e:
                    print(f"  CRASH accessing details: {e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"View error: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"Script error: {e}")
