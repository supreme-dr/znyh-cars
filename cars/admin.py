from django.contrib import admin
from .models import Brand, Car, CarImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3 # Gives you 3 empty slots by default
    fields = ('image', 'view_type', 'is_primary', 'order') # Shows the view type dropdown


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'condition', 'transmission', 'fuel_type', 'is_available', 'is_featured')
    list_filter = ('brand', 'condition', 'transmission', 'fuel_type', 'is_available', 'is_featured')
    search_fields = ('model_name', 'brand__name', 'description')
    prepopulated_fields = {'slug': ('model_name',)}
    inlines = [CarImageInline]