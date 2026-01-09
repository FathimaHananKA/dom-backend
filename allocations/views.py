from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Allocation
from .serializers import AllocationSerializer

from .serializers import MyAccommodationSerializer
from accounts.models import StudentProfile

class MyAccommodationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_profile = request.user.studentprofile
            allocation = Allocation.objects.get(student=student_profile)
            serializer = MyAccommodationSerializer(allocation)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {"message": "User is not a student"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Allocation.DoesNotExist:
            return Response(
                {"message": "Accommodation not allocated yet"},
                status=status.HTTP_404_NOT_FOUND
            )

class AllocationViewSet(ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
