from rest_framework.viewsets import ModelViewSet
from .models import Allocation
from .serializers import AllocationSerializer


class AllocationViewSet(ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
