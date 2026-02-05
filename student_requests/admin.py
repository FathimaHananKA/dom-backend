from django.contrib import admin
from .models import Request, NewStudentRequest

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_room', 'preferred_room', 'status', 'requested_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('student__user__username',)

@admin.register(NewStudentRequest)
class NewStudentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'preferred_dormitory', 'room_type_preference', 'status', 'created_at')
    list_filter = ('status', 'room_type_preference')
    search_fields = ('student__user__username', 'preferred_dormitory__name')

