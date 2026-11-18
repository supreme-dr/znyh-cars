from django import forms
from .models import TestDriveBooking, ServiceAppointment

class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDriveBooking
        fields = ['preferred_date', 'preferred_time']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'class': 'form-control bg-light', 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': 'form-control bg-light', 'type': 'time'}),
        }

class ServiceAppointmentForm(forms.ModelForm):
    class Meta:
        model = ServiceAppointment
        fields = ['car_model', 'service_type', 'preferred_date', 'notes']
        widgets = {
            'car_model': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'e.g., 2015 Toyota Camry'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'e.g., Full Service, Brake Repair'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control bg-light', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control bg-light', 'rows': 3, 'placeholder': 'Tell us a bit more about the issue...'}),
        }
        