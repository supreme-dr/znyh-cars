from django.contrib import admin
from .models import TestDriveBooking, ServiceAppointment

@admin.register(TestDriveBooking)
class TestDriveBookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car', 'preferred_date', 'preferred_time', 'status')
    list_filter = ('status', 'preferred_date')
    search_fields = ('customer__username', 'car__model_name')
    list_editable = ('status',)

@admin.register(ServiceAppointment)
class ServiceAppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car_model', 'service_type', 'preferred_date', 'status')
    list_filter = ('status', 'preferred_date')
    search_fields = ('customer__username', 'car_model', 'service_type')
    list_editable = ('status',)
    