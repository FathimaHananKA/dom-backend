from rest_framework.viewsets import ModelViewSet
from .models import Dormitory
from .serializers import DormitorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DormitoryViewSet(ModelViewSet):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer
    filterset_fields = ['type', 'gender']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_dormitory(self, request):
        try:
            # Assuming the user is a warden and has a WardenProfile
            if hasattr(request.user, 'wardenprofile'):
                dormitory = Dormitory.objects.get(assigned_warden=request.user.wardenprofile)
                serializer = self.get_serializer(dormitory)
                return Response(serializer.data)
            return Response({'detail': 'User is not a warden'}, status=403)
        except Dormitory.DoesNotExist:
            return Response({'detail': 'No dormitory assigned'}, status=404)
