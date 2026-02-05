from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet, DormApplicationCreateView, DormApplicationDetailView, DormApplicationListView, NewStudentRequestViewSet, AdminDormApplicationDetailView, WardenDormApplicationsView

# DRF router for RequestViewSet
router = DefaultRouter()
router.register(r'requests', RequestViewSet, basename='request')
router.register(r'new-student-requests', NewStudentRequestViewSet, basename='new-student-request')

urlpatterns = [
    # Include router urls
    path('', include(router.urls)),

    # Dorm Application endpoints
    path('student/apply/', DormApplicationCreateView.as_view(), name='dorm-apply'),           # POST to apply
    path('student/application/', DormApplicationDetailView.as_view(), name='dorm-application-detail'),  # GET application
    path('applications/', DormApplicationListView.as_view(), name='admin-applications-list'), # Admin list applications
    path('applications/<int:pk>/', AdminDormApplicationDetailView.as_view(), name='admin-application-detail'), # Admin detail/update
    path('warden/applications/', WardenDormApplicationsView.as_view(), name='warden-applications'), # Warden list applications
]
