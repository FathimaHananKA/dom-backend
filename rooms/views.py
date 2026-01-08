from rest_framework.viewsets import ModelViewSet
from .models import Room, Bed
from .serializers import RoomSerializer, BedSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BedViewSet(ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
