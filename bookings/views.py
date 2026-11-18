from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cars.models import Car
from .forms import TestDriveForm, ServiceAppointmentForm

@login_required
def book_test_drive(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    if request.method == 'POST':
        form = TestDriveForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.car = car
            booking.save()
            messages.success(request, "Test drive requested! We will contact you to confirm.")
            return redirect('dashboard')
    else:
        form = TestDriveForm()
        
    return render(request, 'bookings/test_drive_form.html', {'form': form, 'car': car})

@login_required
def book_service(request):
    if request.method == 'POST':
        form = ServiceAppointmentForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, "Service appointment requested! We will confirm shortly.")
            return redirect('dashboard')
    else:
        form = ServiceAppointmentForm()
        
    return render(request, 'bookings/service_form.html', {'form': form})
    