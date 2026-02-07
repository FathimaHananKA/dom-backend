import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from allocations.models import Allocation
from student_requests.models import DormApplication

def cleanup():
    print("--- Synchronizing DormApplication Statuses ---")
    allocations = Allocation.objects.all()
    count = 0
    
    for alloc in allocations:
        student = alloc.student
        # Find pending applications for this student
        pending_apps = DormApplication.objects.filter(student=student, status='PENDING')
        for app in pending_apps:
            app.status = 'APPROVED'
            app.save()
            count += 1
            print(f"Updated application status for {student.user.username} (ID: {student.student_id})")
            
    print(f"\nSuccessfully synchronized {count} application records.")

if __name__ == "__main__":
    cleanup()
