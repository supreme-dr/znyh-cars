from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'car', 'amount', 'reference', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'reference', 'car__model_name')
    