import io
import random
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from cars.models import Brand, Car, CarImage

class Command(BaseCommand):
    help = 'Automatically seed 80 cars with reliable, specific images'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 80 cars into the database...")

        # 1. Create Brands
        brand_names = ["Toyota", "Lexus", "Mercedes-Benz", "Honda", "Hyundai", "Ford", "Kia", "BMW"]
        brands = {}
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands[name] = brand

        # 2. Define car pools and matching image URLs
        car_data = {
            "Toyota": {
                "models": ["Camry", "Corolla", "RAV4", "Highlander", "Prado", "Hilux"],
                "images": [
                    "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80", # Camry
                    "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800&q=80", # Corolla
                    "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80", # RAV4/SUV
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80", # SUV
                ]
            },
            "Lexus": {
                "models": ["RX 350", "GX 460", "ES 350", "LX 570"],
                "images": [
                    "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
                    "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80",
                ]
            },
            "Mercedes-Benz": {
                "models": ["GLE 53 AMG", "C-Class", "E-Class", "G-Wagon", "ML-Class"],
                "images": [
                    "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800&q=80",
                    "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
                    "https://images.unsplash.com/photo-1520031441872-265e4ff70366?w=800&q=80", # G-Wagon
                ]
            },
            "Honda": {
                "models": ["Accord", "Civic", "CR-V", "Pilot"],
                "images": [
                    "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800&q=80",
                    "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80",
                ]
            },
            "Hyundai": {
                "models": ["Elantra", "Tucson", "Santa Fe", "Sonata"],
                "images": [
                    "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80",
                    "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80",
                ]
            },
            "Ford": {
                "models": ["Explorer", "Mustang", "F-150", "Edge"],
                "images": [
                    "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80", # Mustang
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80",
                ]
            },
            "Kia": {
                "models": ["Sportage", "Sorento", "K5", "Telluride"],
                "images": [
                    "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80",
                    "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80",
                ]
            },
            "BMW": {
                "models": ["X5", "3 Series", "5 Series", "X7"],
                "images": [
                    "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
                    "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80",
                ]
            }
        }

        conditions = ['new', 'used', 'certified']
        transmissions = ['automatic', 'manual']
        fuels = ['petrol', 'diesel', 'hybrid']

        car_count = 0
        while car_count < 80:
            # Pick random brand
            brand_name = random.choice(brand_names)
            brand_info = car_data[brand_name]
            
            # Pick random model from that brand
            model_name = random.choice(brand_info["models"])
            
            # Pick an image from that brand's image list
            img_url = random.choice(brand_info["images"])
            
            # Random details
            year = random.randint(2008, 2026)
            condition = random.choice(conditions)
            
            # Price logic
            base_price = random.randint(3000000, 30000000)
            if condition == 'new':
                base_price *= 3
            elif year >= 2020:
                base_price *= 2
                
            price = round(base_price, -4)
            transmission = random.choice(transmissions)
            fuel = random.choice(fuels)

            # Create the car (avoid exact duplicates)
            car, created = Car.objects.get_or_create(
                brand=brands[brand_name],
                model_name=model_name,
                year=year,
                defaults={
                    'price': price,
                    'condition': condition,
                    'transmission': transmission,
                    'fuel_type': fuel,
                    'mileage': random.randint(0, 150000),
                    'color': random.choice(['Black', 'White', 'Silver', 'Gray', 'Blue', 'Red']),
                    'description': f"Excellent {year} {brand_name} {model_name}. Fully loaded and in great condition. Perfect for family or business use.",
                    'is_available': True,
                    'is_featured': True if year >= 2023 else False,
                }
            )

            if created:
                car_count += 1
                self.stdout.write(self.style.SUCCESS(f"[{car_count}/80] Created: {car} - ₦{price}"))
                
                try:
                    # Download the guaranteed image
                    response = requests.get(img_url, timeout=15)
                    
                    if response.status_code == 200:
                        car_image = CarImage(car=car, is_primary=True)
                        car_image.image.save(
                            f"{car.slug}.jpg",
                            File(io.BytesIO(response.content)),
                            save=True
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f"Failed image download for {car}: Status {response.status_code}"))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Could not download image for {car}: {e}"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded 80 cars with images!"))

        