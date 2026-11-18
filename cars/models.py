from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('certified', 'Certified Pre-Owned'),
    ]
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    mileage = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    color = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.brand.name}-{self.model_name}-{self.year}")
            slug = base
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year} {self.brand.name} {self.model_name}"


class CarImage(models.Model):
    VIEW_CHOICES = [
        ('front', 'Front View'),
        ('back', 'Back View'),
        ('side', 'Side View'),
        ('interior', 'Interior'),
        ('other', 'Other'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    view_type = models.CharField(max_length=20, choices=VIEW_CHOICES, default='other')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_view_type_display()} - {self.car}"
    