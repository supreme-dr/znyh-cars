from django.urls import path
from . import views

urlpatterns = [
    path('test-drive/<slug:car_slug>/', views.book_test_drive, name='book_test_drive'),
    path('book-service/', views.book_service, name='book_service'),
]

