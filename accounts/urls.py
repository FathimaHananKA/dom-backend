from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, StudentProfileViewSet, WardenProfileViewSet, current_user
from rest_framework.viewsets import ModelViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'student-profiles', StudentProfileViewSet, basename='student-profile')
router.register(r'warden-profiles', WardenProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/user/', current_user, name='current_user'),
  

]
