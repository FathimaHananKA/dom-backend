from rest_framework.views import APIView
from rest_framework.response import Response
from allocations.models import Allocation
from rooms.models import Bed
from requests.models import Request

class BedOccupancyReport(APIView):
    def get(self, request):
        total_beds = Bed.objects.count()
        occupied_beds = Bed.objects.filter(is_occupied=True).count()
        available_beds = total_beds - occupied_beds

        return Response({
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "available_beds": available_beds
        })


class AllocationReport(APIView):
    def get(self, request):
        allocations = Allocation.objects.select_related('student', 'bed')
        data = [
            {
                "student": alloc.student.user.username,
                "bed": alloc.bed.bed_number,
                "room": alloc.bed.room.room_number,
                "dormitory": alloc.bed.room.dormitory.name
            }
            for alloc in allocations
        ]
        return Response(data)


class RequestReport(APIView):
    def get(self, request):
        requests = Request.objects.select_related('student', 'current_room', 'preferred_room')
        data = [
            {
                "student": req.student.user.username,
                "current_room": req.current_room.room_number if req.current_room else None,
                "preferred_room": req.preferred_room.room_number if req.preferred_room else None,
                "status": req.status
            }
            for req in requests
        ]
        return Response(data)
