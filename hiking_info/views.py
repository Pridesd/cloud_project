from django.shortcuts import render
from datetime import datetime, timezone, timedelta
from .weather import *

# Create your views here.
def index(request):
    return render(
        request,
        'hiking_info/index.html'
    )

def today(request):
    weather_json = get_weather()
    sunrise = datetime.fromtimestamp(weather_json["sys"]["sunrise"])
    sunset = datetime.fromtimestamp(weather_json["sys"]["sunset"])
    dt = datetime.fromtimestamp(weather_json["dt"])
    dt = dt.strftime("%Y년 %m월 %d일 %H:%M 기준")

    weather = {
        "main": weather_json["weather"][0]["main"],
        "icon":  "https://openweathermap.org/img/wn/"+ weather_json["weather"][0]["icon"] +"@2x.png",
        "temp": weather_json["main"]["temp"],
        "humidity": weather_json["main"]["humidity"],
        "wind_speed": weather_json["wind"]["speed"],
        "wind_deg": get_wind_deg(weather_json["wind"]["deg"]),
        "sunrise": get_hour(sunrise),
        "sunset": get_hour(sunset),
        "dt": dt
    }
    return render(
        request,
        'hiking_info/today.html',
        {
            'weather': weather
        }
    )
def forecast(request):
    forecast_list = get_forecast()
    result = []
    for forecast_data in forecast_list:
        datetime_format = "%Y-%m-%d %H:%M:%S"
        datetime_string = forecast_data['dt_txt']
        datetime_result = datetime.strptime(datetime_string, datetime_format)
        datetime_result += timedelta(hours=9)
        datetime_result = datetime_result.strftime('%m월%d일 %H시')

        weather = {
            "main": forecast_data["weather"][0]["main"],
            "icon": "https://openweathermap.org/img/wn/" + forecast_data["weather"][0]["icon"] + "@2x.png",
            "temp": forecast_data["main"]["temp"],
            "humidity": forecast_data["main"]["humidity"],
            "wind_speed": forecast_data["wind"]["speed"],
            "wind_deg": get_wind_deg(forecast_data["wind"]["deg"]),
            "dt": datetime_result
        }
        result.append(weather)
    return render(
        request,
        'hiking_info/forecast.html',
        {
            "forecast_list": result
        }
    )

def cloudsea(request):
    cloud_data = is_cloudsea()
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    tomorrow = now + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y년 %m월 %d일의 운해')

    return render(
        request,
        'hiking_info/cloudsea.html',
        {
            'is_cloudsea': cloud_data['is_cloud'],
            'tomorrow': tomorrow,
            'weather': cloud_data['weather']
        }
    )
