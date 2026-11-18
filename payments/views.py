import uuid
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from cars.models import Car
from .models import Payment

@login_required
def initiate_payment(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    # Deposit is 10% of the car price
    deposit_amount = float(car.price) * 0.10 
    
    if request.method == 'POST':
        # Paystack expects amount in Kobo (multiply by 100)
        amount_in_kobo = int(deposit_amount * 100)
        reference = str(uuid.uuid4())
        
        # Save pending payment to DB
        payment = Payment.objects.create(
            customer=request.user,
            car=car,
            amount=deposit_amount,
            reference=reference,
            status='pending'
        )
        
        # Prepare Paystack API call
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": request.user.email,
            "amount": amount_in_kobo,
            "reference": reference,
            "callback_url": request.build_absolute_uri(f'/payments/verify/{reference}/')
        }
        
        # Send request to Paystack
        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()
        
        # Check if Paystack responded successfully
        if response.status_code == 200 and res_data.get('status'):
            return redirect(res_data['data']['authorization_url'])
            
        # IF IT FAILS, PRINT THE ERROR TO THE TERMINAL AND SHOW IT ON SCREEN
        print("PAYSTACK ERROR:", res_data) 
        messages.error(request, f"Payment failed: {res_data.get('message', 'Unknown error')}")
        return redirect('car_detail', slug=car.slug)
        
    return render(request, 'payments/initiate_payment.html', {
        'car': car,
        'deposit_amount': deposit_amount
    })

@login_required
def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference, customer=request.user)
    
    # Verify with Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        res_data = response.json()
        if res_data.get('status') and res_data['data']['status'] == 'success':
            payment.status = 'success'
            payment.save()
            messages.success(request, f"Payment of ₦{payment.amount} for {payment.car} was successful!")
            return redirect('dashboard')
            
    payment.status = 'failed'
    payment.save()
    messages.error(request, "Payment verification failed.")
    return redirect('car_detail', slug=payment.car.slug)
