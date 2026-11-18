from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from inquiries.models import Inquiry
from bookings.models import TestDriveBooking, ServiceAppointment
from payments.models import Payment


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    inquiries = Inquiry.objects.filter(email=request.user.email)
    test_drives = TestDriveBooking.objects.filter(customer=request.user).select_related('car')
    services = ServiceAppointment.objects.filter(customer=request.user)
    payments = Payment.objects.filter(customer=request.user).select_related('car') # <-- ADD THIS
    
    context = {
        'inquiries': inquiries,
        'test_drives': test_drives,
        'services': services,
        'payments': payments, # <-- ADD THIS
    }
    return render(request, 'accounts/dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('home')
