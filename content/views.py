from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # get_or_create prevents duplicate emails
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")
            
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER', 'home'))
