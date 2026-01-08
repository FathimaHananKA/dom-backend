from django.contrib import admin
from .models import Allocation

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'bed', 'allocated_at')
    search_fields = ('student__user__username',)
