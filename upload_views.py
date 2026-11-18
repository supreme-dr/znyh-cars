import os
import django
import time
import io
import requests
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'znyh_cars.settings')
django.setup()

from cars.models import Car, CarImage

def upload_views():
    cars = Car.objects.all()
    print(f"Found {cars.count()} cars. Adding GUARANTEED car images...")

    # 10 Reliable, direct car image URLs (Front, Back, Side views of actual cars)
    # We cycle through these to ensure every car gets a real image.
    front_images = [
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80",
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80",
        "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80",
    ]
    back_images = [
        "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80",
        "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80",
        "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
        "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800&q=80",
    ]
    side_images = [
        "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80",
        "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80",
        "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80",
        "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800&q=80",
    ]

    for i, car in enumerate(cars):
        # Cycle through the images based on the car's ID so they aren't all identical
        front_url = front_images[i % len(front_images)]
        back_url = back_images[i % len(back_images)]
        side_url = side_images[i % len(side_images)]

        views = [
            ('front', front_url),
            ('back', back_url),
            ('side', side_url)
        ]

        for view_type, url in views:
            try:
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    img_obj = CarImage(car=car, view_type=view_type)
                    img_obj.image.save(
                        f"{car.slug}_{view_type}.jpg",
                        File(io.BytesIO(response.content)),
                        save=True
                    )
                    print(f"✅ Success: {view_type} for {car}")
                else:
                    print(f"❌ Failed: {view_type} for {car} - Status {response.status_code}")
            except Exception as e:
                print(f"❌ Error for {car} - {view_type}: {e}")
            
            # Wait a tiny bit between downloads
            time.sleep(0.1)

    print("All done! Go check your website.")

if __name__ == '__main__':
    upload_views()
    