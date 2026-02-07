import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import StudentProfile
from student_requests.models import Request, DormApplication, NewStudentRequest

def audit_pending():
    print("--- Student Request Audit ---")
    students = StudentProfile.objects.all()
    
    for s in students:
        # Check if they have an allocation
        has_alloc = hasattr(s, 'allocation') and s.allocation is not None
        
        # Check for pending things
        p_reqs = Request.objects.filter(student=s, status='Pending')
        p_apps = DormApplication.objects.filter(student=s, status='PENDING')
        p_new = NewStudentRequest.objects.filter(student=s, status='Pending')
        
        any_pending = p_reqs.exists() or p_apps.exists() or p_new.exists()
        
        if (has_alloc and any_pending) or (not has_alloc and not any_pending):
            print(f"\nStudent: {s.user.username} (ID: {s.student_id})")
            print(f"Allocated: {has_alloc}")
            if p_reqs.exists(): print(f"  - Pending Room Changes: {p_reqs.count()}")
            if p_apps.exists(): print(f"  - Pending Applications: {p_apps.count()}")
            if p_new.exists(): print(f"  - Pending New Student Requests: {p_new.count()}")

if __name__ == "__main__":
    audit_pending()
