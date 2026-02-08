import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile
from payments.models import Payment
from allocations.models import Allocation

User = get_user_model()

def check_payment_status():
    username = 'Athira'
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"User {username} not found")
        return

    print(f"User: {user.username} (ID: {user.id})")
    
    if not hasattr(user, 'studentprofile'):
        print("No student profile")
        return
        
    student_profile = user.studentprofile
    print(f"Student Profile ID: {student_profile.id}")
    
    # Check Allocations
    try:
        allocation = Allocation.objects.get(student=student_profile)
        print(f"Allocation Found: ID {allocation.id}, is_paid={allocation.is_paid}")
        print(f"Allocation is linked to Bed: {allocation.bed}")
    except Allocation.DoesNotExist:
        print("No allocation found for student.")
        allocation = None

    # Check Payments for Student
    print("\n--- Payments linked to Student ---")
    payments = Payment.objects.filter(student=student_profile)
    for p in payments:
        print(f"Payment ID: {p.id}")
        print(f"  Status: {p.status}")
        print(f"  Amount: {p.amount}")
        print(f"  Order ID: {p.razorpay_order_id}")
        print(f"  Linked to Allocation ID: {p.allocation_id}")
        
        if allocation and p.allocation_id == allocation.id:
             print("  -> MATCHES CURRENT ALLOCATION")
        else:
             print("  -> DOES NOT MATCH CURRENT ALLOCATION")

if __name__ == "__main__":
    check_payment_status()
