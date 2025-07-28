# src/weather_connector.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_forecast(city, api_key=API_KEY):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'fr'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for entry in data['list']:
            forecasts.append({
                'datetime': entry['dt_txt'],
                'temp': entry['main']['temp'],
                'humidity': entry['main']['humidity'],
                'description': entry['weather'][0]['description']
            })
        return forecasts
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")
