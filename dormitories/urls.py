from rest_framework.routers import DefaultRouter
from .views import DormitoryViewSet

router = DefaultRouter()
router.register(r'dormitories', DormitoryViewSet, basename='dormitory')

urlpatterns = router.urls
