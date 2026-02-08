from rest_framework.views import APIView
from rest_framework.response import Response
from allocations.models import Allocation
from rooms.models import Bed
from student_requests.models import Request
from payments.models import Payment
from accounts.models import StudentProfile

class BedOccupancyReport(APIView):
    def get(self, request):
        # Default querysets
        beds = Bed.objects.all()
        
        # Filter by warden's dormitory if user is a warden
        if hasattr(request.user, 'wardenprofile'):
            from dormitories.models import Dormitory
            warden_dorms = Dormitory.objects.filter(assigned_warden=request.user.wardenprofile)
            if warden_dorms.exists():
                beds = beds.filter(room__dormitory__in=warden_dorms)
        
        total_beds = beds.count()
        occupied_beds = beds.filter(is_occupied=True).count()
        available_beds = total_beds - occupied_beds

        return Response({
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "available_beds": available_beds
        })


class AllocationReport(APIView):
    def get(self, request):
        allocations = Allocation.objects.select_related('student', 'student__user', 'bed', 'bed__room', 'bed__room__dormitory').prefetch_related('payments')
        
        # Filter by warden's dormitory if user is a warden
        if hasattr(request.user, 'wardenprofile'):
            from dormitories.models import Dormitory
            warden_dorms = Dormitory.objects.filter(assigned_warden=request.user.wardenprofile)
            if warden_dorms.exists():
                allocations = allocations.filter(bed__room__dormitory__in=warden_dorms)
        
        data = []
        for alloc in allocations:
            data.append({
                "student": alloc.student.user.username,
                "student_id": alloc.student.student_id,
                "email": alloc.student.user.email,
                "phone": getattr(alloc.student, 'phone', 'N/A'),
                "department": alloc.student.department,
                "year": alloc.student.year,
                "bed": alloc.bed.bed_number,
                "room": alloc.bed.room.room_number,
                "dormitory": alloc.bed.room.dormitory.name,
                "allocated_at": alloc.allocated_at,
                "is_paid": alloc.is_paid or alloc.payments.filter(status='SUCCESS').exists()
            })
        return Response(data)


class RequestReport(APIView):
    def get(self, request):
        requests = Request.objects.select_related('student', 'student__user', 'current_room', 'preferred_dormitory')
        
        # Filter logic can be added here similar to other reports if needed
        
        data = [
            {
                "student": req.student.user.username,
                "student_id": req.student.student_id,
                "current_room": req.current_room.room_number if req.current_room else "N/A",
                "preferred_dorm": req.preferred_dormitory.name if req.preferred_dormitory else "Any",
                "room_type_preference": req.room_type_preference,
                "status": req.status,
                "requested_at": req.requested_at
            }
            for req in requests
        ]
        return Response(data)

class PaymentReport(APIView):
    def get(self, request):
        # Admin only for now
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)

        payments = Payment.objects.select_related('student', 'student__user', 'allocation', 'allocation__bed__room__dormitory').order_by('-created_at')
        
        data = []
        for p in payments:
            dorm_name = "N/A"
            if p.allocation and p.allocation.bed and p.allocation.bed.room and p.allocation.bed.room.dormitory:
                dorm_name = p.allocation.bed.room.dormitory.name
                
            data.append({
                "id": p.id,
                "student": p.student.user.username,
                "student_id": p.student.student_id,
                "amount": p.amount,
                "status": p.status,
                "razorpay_order_id": p.razorpay_order_id,
                "razorpay_payment_id": p.razorpay_payment_id or "N/A",
                "date": p.created_at,
                "dormitory": dorm_name
            })
        return Response(data)

class StudentReport(APIView):
    def get(self, request):
        # Admin only
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
            
        profiles = StudentProfile.objects.select_related('user', 'allocation', 'allocation__bed__room__dormitory').prefetch_related('allocation__payments')
        
        data = []
        for p in profiles:
            allocation_status = "Unallocated"
            dorm_name = "N/A"
            room_no = "N/A"
            is_paid = "N/A"
            
            if hasattr(p, 'allocation') and p.allocation:
                allocation_status = "Allocated"
                dorm_name = p.allocation.bed.room.dormitory.name
                room_no = p.allocation.bed.room.room_number
                # Check for is_paid flag OR exists successful payment
                paid_status = p.allocation.is_paid or p.allocation.payments.filter(status='SUCCESS').exists()
                is_paid = "Paid" if paid_status else "Pending Payment"
            
            data.append({
                "username": p.user.username,
                "full_name": p.user.get_full_name(),
                "student_id": p.student_id,
                "email": p.user.email,
                "phone": getattr(p, 'phone', 'N/A'),
                "department": p.department,
                "year": p.year,
                "status": allocation_status,
                "dormitory": dorm_name,
                "room": room_no,
                "payment_status": is_paid
            })
        return Response(data)
