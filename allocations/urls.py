from rest_framework.routers import DefaultRouter
from .views import AllocationViewSet

router = DefaultRouter()
router.register(r'allocations', AllocationViewSet, basename='allocation')

urlpatterns = router.urls
