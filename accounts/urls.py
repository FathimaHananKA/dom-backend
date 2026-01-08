from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, StudentProfileViewSet, WardenProfileViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'warden-profiles', WardenProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]