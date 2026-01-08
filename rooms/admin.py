from django.contrib import admin
from .models import Room, Bed


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'dormitory')
    list_filter = ('dormitory',)
    search_fields = ('room_number',)


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'room', 'is_occupied')
    list_filter = ('is_occupied', 'room')
    search_fields = ('bed_number',)
