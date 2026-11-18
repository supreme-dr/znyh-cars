from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car, Brand


def home(request):
    featured_cars = Car.objects.filter(is_available=True, is_featured=True)[:6]
    latest_cars = Car.objects.filter(is_available=True)[:6]
    brands = Brand.objects.all()

    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'brands': brands,
    }
    return render(request, 'cars/home.html', context)


def car_list(request):
    cars = Car.objects.filter(is_available=True).select_related('brand')

    # Filters
    q = request.GET.get('q', '').strip()
    brand = request.GET.get('brand', '').strip()
    condition = request.GET.get('condition', '').strip()
    transmission = request.GET.get('transmission', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if q:
        cars = cars.filter(
            Q(model_name__icontains=q) |
            Q(brand__name__icontains=q) |
            Q(description__icontains=q)
        )
    if brand:
        cars = cars.filter(brand__id=brand)
    if condition:
        cars = cars.filter(condition=condition)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'brands': Brand.objects.all(),
        'condition_choices': Car.CONDITION_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'filters': {
            'q': q,
            'brand': brand,
            'condition': condition,
            'transmission': transmission,
            'min_price': min_price,
            'max_price': max_price,
        },
    }
    return render(request, 'cars/car_list.html', context)


def car_detail(request, slug):
    car = get_object_or_404(
        Car.objects.select_related('brand').prefetch_related('images'),
        slug=slug,
    )
    similar_cars = Car.objects.filter(
        brand=car.brand, is_available=True
    ).exclude(pk=car.pk)[:4]

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'similar_cars': similar_cars,
    })
