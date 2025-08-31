from django.contrib import admin
from .models import AvailabilitySlot, Booking

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('tasker', 'date', 'start_time', 'end_time', 'is_booked', 'id')
    list_filter = ('date', 'is_booked', 'tasker')
    search_fields = ('tasker__username', 'tasker__email')
    ordering = ('date', 'start_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'tasker', 'task', 'date', 'start_time', 'status')
    list_filter = ('status', 'availability_slot__date', 'task')
    search_fields = ('client__username', 'tasker__username', 'task__name')
    ordering = ('-created_at',)
    
    def date(self, obj):
        return obj.availability_slot.date
    date.short_description = 'Date'
    
    def start_time(self, obj):
        return obj.availability_slot.start_time
    start_time.short_description = 'Start Time'
