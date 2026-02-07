import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from student_requests.models import Request, DormApplication
from allocations.models import Allocation
from accounts.models import StudentProfile

def test_approval():
    print("--- Testing Approval Flow ---")
    
    # 1. Test Request (Room Change) Approval
    req = Request.objects.filter(status='Pending').first()
    if req:
        print(f"Testing Room Change Request Approval for ID: {req.id}")
        # Mark as approved
        req.status = 'Approved'
        req.save()
        # Fetch again
        req.refresh_from_db()
        print(f"New Status: {req.status}")
        if req.status == 'Approved':
            print("SUCCESS: Request status updated.")
        else:
            print("FAILED: Request status not updated.")
    else:
        print("No pending room change requests found.")

    # 2. Test DormApplication Approval
    app = DormApplication.objects.filter(status='PENDING').first()
    if app:
        print(f"\nTesting DormApplication Approval for ID: {app.id}")
        # Mark as APPROVED
        app.status = 'APPROVED'
        app.save()
        # Fetch again
        app.refresh_from_db()
        print(f"New Status: {app.status}")
        if app.status == 'APPROVED':
            print("SUCCESS: Application status updated.")
        else:
            print("FAILED: Application status not updated.")
    else:
        print("No pending dorm applications found.")

if __name__ == "__main__":
    test_approval()
