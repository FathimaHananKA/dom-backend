from rest_framework.viewsets import ModelViewSet
from .models import Dormitory
from .serializers import DormitorySerializer

class DormitoryViewSet(ModelViewSet):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer
