from django.urls import path
from . import views

urlpatterns = [
    path('pay/<slug:car_slug>/', views.initiate_payment, name='initiate_payment'),
    path('payments/verify/<str:reference>/', views.verify_payment, name='verify_payment'),
]

