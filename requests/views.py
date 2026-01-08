from rest_framework.viewsets import ModelViewSet
from .models import Request
from .serializers import RequestSerializer

class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
