from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AllocationViewSet, MyAccommodationView


router = DefaultRouter()
router.register(r'allocations', AllocationViewSet, basename='allocation')

urlpatterns = [
    path('', include(router.urls)),
    path('my-accomodation/', MyAccommodationView.as_view()),
]