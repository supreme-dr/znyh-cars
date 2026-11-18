from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('', include('inquiries.urls')),
    path('accounts/', include('accounts.urls')), 
    path('bookings/', include('bookings.urls')), 
    path('', include('payments.urls')),
    path('', include('content.urls')), # <--- ADD THIS LINE
]
# THIS PART IS VERY IMPORTANT FOR IMAGES:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    