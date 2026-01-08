from django.urls import path
from .views import BedOccupancyReport, AllocationReport, RequestReport

urlpatterns = [
    path('bed-occupancy/', BedOccupancyReport.as_view(), name='bed-occupancy-report'),
    path('allocations/', AllocationReport.as_view(), name='allocation-report'),
    path('requests/', RequestReport.as_view(), name='requests-report'),
]
