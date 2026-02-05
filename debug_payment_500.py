import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import StudentProfile
from payments.models import Payment
from payments.serializers import PaymentDetailSerializer
from allocations.models import Allocation

def debug_payment_status():
    print("Starting Debug...")
    
    # Iterate over all students with allocations
    profiles = StudentProfile.objects.all()
    print(f"Found {profiles.count()} student profiles")

    for student_profile in profiles:
        print(f"\nEvaluating Student: {student_profile.student_id} ({student_profile.user.username})")
        
        try:
            allocation = student_profile.allocation
            print(f"  Allocation found: ID {allocation.id}")
            print(f"  Allocation is_paid: {allocation.is_paid}")
        except Exception as e:
            print(f"  No allocation or error: {e}")
            continue

        # Check Bed/Room/Dorm chain
        try:
            bed = allocation.bed
            print(f"  Bed: {bed}")
            room = bed.room
            print(f"  Room: {room}")
            dorm = room.dormitory
            print(f"  Dorm: {dorm.name}")
            # Check for warden
            try:
                warden = dorm.warden
                print(f"  Warden: {warden}")
            except Exception as e:
                print(f"  No warden or error: {e}")

        except Exception as e:
            print(f"  Error accessing bed/room/dorm chain: {e}")
            # This would definitely cause a 500 in the 'else' block
            continue

        # Check Payment Logic
        try:
            payment = Payment.objects.filter(
                student=student_profile,
                allocation=allocation
            ).order_by('-created_at').first()

            if payment:
                print(f"  Payment found: ID {payment.id}")
                # Try serializing
                try:
                    serializer = PaymentDetailSerializer(payment)
                    data = serializer.data
                    print("  Serializer SUCCESS")
                except Exception as e:
                    print(f"  Serializer FAILED: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("  No payment found (Entering 'else' block logic)")
                # Simulate the else block dictionary construction
                try:
                    data = {
                        'dormitory_name': allocation.bed.room.dormitory.name if allocation.bed else None,
                        'room_number': allocation.bed.room.room_number if allocation.bed else None,
                        'room_type': allocation.bed.room.room_type if allocation.bed else None,
                        'bed_number': allocation.bed.bed_number if allocation.bed else None,
                    }
                    print("  Else block logic SUCCESS")
                except Exception as e:
                    print(f"  Else block logic FAILED: {e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"  General error during logic: {e}")

if __name__ == '__main__':
    try:
        debug_payment_status()
    except Exception as e:
        print(f"Top level error: {e}")
