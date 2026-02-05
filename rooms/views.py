from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, Bed
from .serializers import RoomSerializer, BedSerializer, WardenRoomDetailSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def warden_rooms(self, request):
        """
        Fetch detailed room information for the warden's assigned dormitory
        """
        try:
            # Check if user is a warden
            if not hasattr(request.user, 'wardenprofile'):
                return Response({'detail': 'User is not a warden'}, status=403)
            
            # Get warden's assigned dormitory
            from dormitories.models import Dormitory
            dormitory = Dormitory.objects.get(assigned_warden=request.user.wardenprofile)
            
            # Get all rooms for this dormitory
            rooms = Room.objects.filter(dormitory=dormitory).prefetch_related('beds', 'beds__allocation', 'beds__allocation__student', 'beds__allocation__student__user')
            
            # Use detailed serializer
            serializer = WardenRoomDetailSerializer(rooms, many=True)
            return Response(serializer.data)
            
        except Dormitory.DoesNotExist:
            return Response({'detail': 'No dormitory assigned'}, status=404)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


class BedViewSet(ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
