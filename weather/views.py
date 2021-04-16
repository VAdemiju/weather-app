<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import City
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def home(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            place = request.POST.get('place')
            if place and not City.objects.filter(name=place, user=request.user):
                pending_city = City(name=place, user=request.user)
                url = f"https://api.openweathermap.org/data/2.5/weather?q={pending_city}&appid=d84ae1a62c6424c03582444686d74930"
                r = requests.get(url).json()
                if r.get('main'):
                    pending_city.save()
        else: return redirect(reverse('account:login'))
    if request.user.is_authenticated:
        cities = City.objects.filter(user=request.user)
    else: cities = City.objects.all()[:5]

    weather_data = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=d84ae1a62c6424c03582444686d74930"
        r = requests.get(url).json()

        city_weather = {
            'obj': city,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {"weather_data":weather_data}
    return render(request, 'index.html', context)



@login_required
def delete(request, name_slug, id):
    city = City.objects.get(id=id, name_slug=name_slug)
    city.delete()
    return redirect("weather:home")
=======
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')
>>>>>>> parent of 5696d89 (Updated the weather app)
