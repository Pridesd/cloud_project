import joblib
import requests
import json
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np

#북한산 인근 지역으로 기상 정보를 가지고 옴
appid = "dd067a9aa888d5941ce0662190c0a2f4"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast?lat=37.6387&lon=127.0370&appid="+ appid +"&units=metric"
current_url = "https://api.openweathermap.org/data/2.5/weather?lat=37.6387&lon=127.0370&units=metric&appid="+appid

def get_forecast():
    response = requests.get(forecast_url)
    json_data = response.json()
    s1 = json.dumps(json_data)
    json_object = json.loads(s1)
    forecast_list = json_object['list']

    return forecast_list
def get_weather():
    response = requests.get(current_url)
    json_data = response.json()
    s1 = json.dumps(json_data)
    json_object = json.loads(s1)

    return json_object

def is_cloudsea():
    forecast_list = get_forecast()

    days = []

    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    days.append(now.strftime('%Y-%m-%d'))
    for i in range(1, 5):
        day = now + timedelta(days=i)
        days.append(day.strftime('%Y-%m-%d'))
    midnight = "00:00:00"
    sunrise = "06:00:00"

    df = pd.DataFrame(index=[1])
    pre_temp = 0

    for forecast in forecast_list:

        # API 결과 값에서 나오는 시간은 UTC(영국) 기준이기 때문에 9시간을 더해줘야 함
        datetime_format = "%Y-%m-%d %H:%M:%S"
        datetime_string = forecast['dt_txt']
        datetime_result = datetime.strptime(datetime_string, datetime_format)
        datetime_result += timedelta(hours=9)
        day = datetime_result.strftime('%Y-%m-%d')
        daytime = datetime_result.strftime('%H:%M:%S')

        if day == days[1]:
            if daytime == midnight:
                new_columns = ['Previous Temperature', 'Previous Precipitation', 'Previous Humidity',
                              'Previous Pressure']
                pre_temp = float(forecast['main']['temp'])
                rain = 0
                humidity = forecast['main']['humidity']
                pressure = forecast['main']['pressure']
                if forecast['weather'][0]['main'] == 'Rain':
                    rain = forecast['rain']['3h']
                df[new_columns] = pd.Series([pre_temp, rain, humidity, pressure])
                continue

            if daytime == sunrise:
                new_columns = ['Sunrise Temperature', 'Sunrise Wind Speed', 'Sunrise Humidity', 'Sunrise Pressure',
                              'Sunrise Cloud Coverage', 'Diurnal Temperature Range']
                temp = forecast['main']['temp']
                wind = forecast['wind']['speed']
                humidity = forecast['main']['humidity']
                pressure = forecast['main']['pressure']
                clouds = float(forecast['clouds']['all']) / 10
                temp_range = float(temp) - pre_temp
                df[new_columns] = pd.Series([temp, wind, humidity, pressure, clouds, temp_range])
                continue
    ada_clf = joblib.load('learning_model/ada.pkl')
    dt_clf = joblib.load('learning_model/dt.pkl')
    knn_clf = joblib.load('learning_model/knn.pkl')
    rf_clf = joblib.load('learning_model/rf.pkl')
    lr_clf = joblib.load('learning_model/lr.pkl')

    ada = ada_clf.predict(df)
    dt = dt_clf.predict(df)
    knn = knn_clf.predict(df)
    rf = rf_clf.predict(df)
    lr = lr_clf.predict(df)

    stacked = np.array([knn, rf, dt, ada, lr])
    stacked = np.transpose(stacked)

    xgbc = joblib.load('learning_model/xgbc.pkl')
    final_pred = xgbc.predict(stacked)

    return final_pred[0]
