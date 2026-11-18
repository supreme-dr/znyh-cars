from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from urllib.parse import quote
from cars.models import Car
from .forms import InquiryForm

def inquiry_create(request, car_slug=None):
    car = None
    if car_slug:
        car = Car.objects.filter(slug=car_slug).first()

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # 1. Save the inquiry to the database
            inquiry = form.save(commit=False)
            inquiry.car = car
            inquiry.save()
            
            # 2. Prepare the WhatsApp message
            whatsapp_number = getattr(settings, 'WHATSAPP_NUMBER', '')
            
            # Format the message
            text = f"Hello ZNYH Cars! My name is {inquiry.name}.\n"
            if car:
                text += f"I am interested in the {car.year} {car.brand.name} {car.model_name} (₦{car.price:,.0f}).\n"
            else:
                text += f"I have a general inquiry.\n"
            text += f"Phone: {inquiry.phone}\n"
            text += f"Email: {inquiry.email}\n"
            text += f"Message: {inquiry.message}"
            
            # Encode the text for URL
            encoded_text = quote(text)
            
            # Create the WhatsApp URL
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_text}"
            
            messages.success(request, "Your message has been saved! Redirecting you to WhatsApp...")
            
            # 3. Redirect directly to WhatsApp
            return redirect(whatsapp_url)
    else:
        form = InquiryForm()

    return render(request, 'inquiries/inquiry_form.html', {
        'form': form,
        'car': car,
    })

def inquiry_success(request):
    return render(request, 'inquiries/inquiry_success.html')