from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet, DormApplicationCreateView, DormApplicationDetailView

# DRF router for RequestViewSet
router = DefaultRouter()
router.register(r'requests', RequestViewSet, basename='request')

urlpatterns = [
    # Include router urls
    path('', include(router.urls)),

    # Dorm Application endpoints
    path('student/apply/', DormApplicationCreateView.as_view(), name='dorm-apply'),           # POST to apply
    path('student/application/', DormApplicationDetailView.as_view(), name='dorm-application-detail'),  # GET application
]
