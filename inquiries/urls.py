from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.inquiry_create, name='contact'),
    path('contact/car/<slug:car_slug>/', views.inquiry_create, name='inquiry_car'),
    path('contact/success/', views.inquiry_success, name='inquiry_success'),
]

