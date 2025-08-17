import streamlit as st
import requests
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Ajout du chemin vers le dossier src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from air_quality_connector import get_air_quality

# Chargement des variables d'environnement
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 🎨 Dictionnaire des couleurs et labels AQI
aqi_colors = {
    1: ("🟢 Très bonne", "#00e400"),
    2: ("🟡 Bonne", "#ffff00"),
    3: ("🟠 Moyenne", "#ff7e00"),
    4: ("🔴 Mauvaise", "#ff0000"),
    5: ("🟣 Très mauvaise", "#8f3f97")
}

def get_coordinates(city, api_key):
    """
    Récupère les coordonnées géographiques d'une ville via l'API OpenWeather.
    """
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    response = requests.get(base_url, params=params)

    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return data['lat'], data['lon']
    else:
        return None, None

def run():
    """
    Lancement de l'application Streamlit pour afficher la qualité de l'air.
    """
    st.set_page_config(page_title="Qualité de l'air", layout="wide")
    st.title("🌬️ Qualité de l'air dans votre ville")

    city = st.text_input("Entrez le nom d'une ville", "Tunis")

    if not city:
        st.info("📝 Veuillez entrer une ville.")
        return

    lat, lon = get_coordinates(city, API_KEY)

    if lat is None or lon is None:
        st.warning("⚠️ Ville introuvable. Vérifiez l'orthographe.")
        return

    st.success(f"Coordonnées de {city} : {lat}, {lon}")
    st.subheader(f"🌫️ Analyse de la qualité de l'air à {city}")

    try:
        aqi_response = get_air_quality(lat, lon)

        # 🧠 OpenWeather retourne une liste sous la clé "list"
        if aqi_response and "list" in aqi_response and len(aqi_response["list"]) > 0:
            aqi_data = aqi_response["list"][0]
            aqi = aqi_data.get("main", {}).get("aqi", 0)
            components = aqi_data.get("components", {})
        else:
            aqi = 0
            components = {}

        label, color = aqi_colors.get(aqi, ("⚫ Inconnu", "#9e9e9e"))

        st.markdown(
            f"<div style='background-color: {color}; padding: 10px; border-radius: 8px; color: white; text-align: center;'>"
            f"<b>Qualité de l'air : {label}</b></div>",
            unsafe_allow_html=True
        )

        st.metric("Indice AQI", aqi)
        st.markdown("#### Composants mesurés :")
        if components:
            for comp, val in components.items():
                st.write(f"{comp.upper()} : {val} µg/m³")
        else:
            st.warning("❌ Composants indisponibles.")

    except Exception as e:
        st.error(f"Erreur lors de la récupération de l'AQI : {e}")

    st.subheader("📍 Localisation")
    st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))
