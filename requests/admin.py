from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_room', 'preferred_room', 'status', 'requested_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('student__user__username',)
