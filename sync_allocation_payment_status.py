import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from payments.models import Payment
from allocations.models import Allocation

def sync_payment_status():
    print("Starting Payment-Allocation Status Synchronization...")
    
    # 1. Find all successful payments
    successful_payments = Payment.objects.filter(status='SUCCESS')
    print(f"Found {successful_payments.count()} successful payments.")
    
    updated_count = 0
    already_synced_count = 0
    errors_count = 0
    
    for payment in successful_payments:
        try:
            allocation = payment.allocation
            if not allocation:
                print(f"WARNING: Payment {payment.id} (Order: {payment.razorpay_order_id}) has NO associated allocation.")
                continue
                
            if not allocation.is_paid:
                print(f"Updating Allocation {allocation.id} for Student {payment.student.user.username}: is_paid False -> True")
                allocation.is_paid = True
                allocation.save()
                updated_count += 1
            else:
                already_synced_count += 1
                
        except Exception as e:
            print(f"ERROR processing payment {payment.id}: {e}")
            errors_count += 1
            
    print("\nSynchronization Complete.")
    print(f"Updated: {updated_count}")
    print(f"Already Synced: {already_synced_count}")
    print(f"Errors: {errors_count}")

if __name__ == "__main__":
    sync_payment_status()
