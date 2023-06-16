from django.shortcuts import render
from .weather import *

# Create your views here.
def index(request):
    return render(
        request,
        'hiking_info/index.html'
    )

def today(request):
    weather_json = get_weather()
    weather = {
        "main": weather_json["weather"][0]["main"],
        "temp": weather_json["main"]["temp"],
    }
    return render(
        request,
        'hiking_info/today.html',
        {
            'weather': weather
        }
    )
def forecast(request):
    forecast = get_forecast()
    return render(
        request,
        'hiking_info/forecast.html'
    )

def cloudsea(request):
    is_cloud = is_cloudsea()
    return render(
        request,
        'hiking_info/cloudsea.html',
        {
            'is_cloudsea': is_cloud
        }
    )
