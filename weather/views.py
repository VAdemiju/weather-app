from django.shortcuts import render, redirect
from .models import City
import requests

# Create your views here.
def home(request):
    if request.method == "POST":
        place = request.POST.get('place')
        if place and not City.objects.filter(name=place):
            pending_city = City(name=place)
            url = f"https://api.openweathermap.org/data/2.5/weather?q={pending_city}&appid=d84ae1a62c6424c03582444686d74930"
            r = requests.get(url).json()
            if r.get('main').get('temp'):
                pending_city.save()
    cities = City.objects.all()

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



def delete(request, name_slug, id):
    city = City.objects.get(id=id, name_slug=name_slug)
    city.delete()
    return redirect("weather:home")