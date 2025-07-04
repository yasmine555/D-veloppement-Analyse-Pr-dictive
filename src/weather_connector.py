import os
import requests
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_forecast(city, api_key):
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
                'description': entry['weather'][0]['description']
            })
        return forecasts
    else:
        print("Erreur:", response.status_code, response.text)
        return []

# 🔍 Exemple d'utilisation :
if __name__ == "__main__":
    city = "Tunis"
    if not API_KEY:
        print("Clé API manquante. Vérifie ton fichier .env.")
    else:
        forecast = get_weather_forecast(city, API_KEY)
        for f in forecast[:5]:  # Affiche les 5 premières prévisions
            print(f)
