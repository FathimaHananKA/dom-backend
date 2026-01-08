from rest_framework.routers import DefaultRouter
from .views import RequestViewSet

router = DefaultRouter()
router.register(r'requests', RequestViewSet, basename='request')

urlpatterns = router.urls
