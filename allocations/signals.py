from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Allocation
from student_requests.models import DormApplication

@receiver(post_delete, sender=Allocation)
def free_bed_on_allocation_delete(sender, instance, **kwargs):
    """
    Signal to automatically mark the associated bed as unoccupied
    when an Allocation is deleted.
    """
    if instance.bed:
        # Check if the bed still exists (it might be deleted too)
        try:
            bed = instance.bed
            bed.is_occupied = False
            bed.save()
            print(f"Signal: Marked {bed} as available after allocation deletion.")
        except Exception as e:
            print(f"Signal Error: Could not update bed status: {e}")

@receiver(post_save, sender=Allocation)
def approve_requests_on_allocation(sender, instance, created, **kwargs):
    """
    Signal to automatically mark the student's DormApplication, Request,
    and NewStudentRequest as APPROVED/Approved when an Allocation is created or updated.
    """
    try:
        from student_requests.models import DormApplication, Request, NewStudentRequest
        student = instance.student
        
        # 1. Update initial applications
        DormApplication.objects.filter(student=student, status='PENDING').update(status='APPROVED')
        
        # 2. Update room change requests
        Request.objects.filter(student=student, status='Pending').update(status='Approved')
        
        # 3. Update new student requests
        NewStudentRequest.objects.filter(student=student, status='Pending').update(status='Approved')
        
        print(f"Signal: Automatically approved all pending requests for {student.user.username}")
    except Exception as e:
        print(f"Signal Error: Could not update request statuses: {e}")
