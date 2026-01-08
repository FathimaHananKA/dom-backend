from django.urls import path
from .views import hello_world

urlpatterns = [
    path('', hello_world),  # This will handle /api
    path('hello', hello_world),  # This will handle /api/hello
    
]
