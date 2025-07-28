import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from air_quality_connector import get_air_quality
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_coordinates(city, api_key):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return data['lat'], data['lon']
    else:
        return None, None

def run():
    st.title("🌍 Qualité de l'air dans votre ville")

    city = st.text_input("Entrez le nom d'une ville", "Tunis")

    if city:
        lat, lon = get_coordinates(city, API_KEY)

        if lat is not None and lon is not None:
            st.success(f"Coordonnées de {city} : {lat}, {lon}")
            data = get_air_quality(lat, lon)
            
            if data:
                st.subheader("Données de qualité de l'air")
                st.write(data)

                st.metric("AQI (Air Quality Index)", data.get("aqi", "N/A"))
                components = data.get("components", {})
                for comp, val in components.items():
                    st.write(f"{comp.upper()}: {val} µg/m3")
            else:
                st.error("Impossible de récupérer les données de qualité de l'air.")
        else:
            st.warning("Ville non trouvée. Vérifiez l'orthographe.")
