from django.contrib import admin
from .models import Dormitory

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'total_rooms', 'assigned_warden')
    list_filter = ('gender',)
    search_fields = ('name',)
