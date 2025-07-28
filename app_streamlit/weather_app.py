# 📁 app_streamlit/weather_app.py

import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import requests
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from weather_connector import get_weather_forecast
from air_quality_connector import get_air_quality

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def run():
    st.set_page_config(page_title="Météo & Qualité de l'air", layout="wide")
    st.title("🌤️ Tableau de bord - Météo & Qualité de l'air")

    city_by_country = {
        "France": ["Paris", "Lyon", "Marseille", "Toulouse"],
        "Tunisie": ["Tunis", "Sfax", "Sousse", "Gabès"],
        "Italie": ["Rome", "Milan", "Naples", "Florence"],
        "Espagne": ["Madrid", "Barcelone", "Séville", "Valence"],
        "Turquie": ["Istanbul", "Ankara", "Izmir", "Bursa"]
    }

    aqi_colors = {
        1: ("🟢 Très bonne", "#00e400"),
        2: ("🟡 Bonne", "#ffff00"),
        3: ("🟠 Moyenne", "#ff7e00"),
        4: ("🔴 Mauvaise", "#ff0000"),
        5: ("🟣 Très mauvaise", "#8f3f97")
    }

    def get_coordinates(city, api_key):
        base_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city, "limit": 1, "appid": api_key}
        response = requests.get(base_url, params=params)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()[0]
            return data['lat'], data['lon']
        else:
            return None, None

    # Interface utilisateur
    country = st.selectbox("🌍 Choisissez un pays", list(city_by_country.keys()))
    city = st.selectbox("🏙️ Choisissez une ville", city_by_country[country])

    lat, lon = get_coordinates(city, API_KEY)

    if lat is None or lon is None:
        st.warning("⚠️ Ville introuvable. Vérifiez l'orthographe.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🌦️ Prévisions météo pour {city}")
        try:
            data = get_weather_forecast(city)
            df = pd.DataFrame(data)

            st.success("Prévisions pour les 5 jours à venir")

            fig_temp = px.line(df, x="datetime", y="temp", title="🌡️ Température")
            st.plotly_chart(fig_temp, use_container_width=True)

            fig_humidity = px.line(df, x="datetime", y="humidity", title="💧 Humidité")
            st.plotly_chart(fig_humidity, use_container_width=True)

            st.markdown("### 🌥️ Description météo")
            st.dataframe(df[["datetime", "description"]].head(10))

        except Exception as e:
            st.error(f"Erreur météo : {e}")

    with col2:
        st.subheader(f"🌬️ Qualité de l'air à {city}")
        try:
            aqi_data = get_air_quality(lat, lon)
            if aqi_data:
                aqi = aqi_data.get("aqi", 0)
                components = aqi_data.get("components", {})
                label, color = aqi_colors.get(aqi, ("⚫ Inconnu", "#9e9e9e"))

                st.markdown(
                    f"<div style='background-color: {color}; padding: 10px; border-radius: 8px; color: white; text-align: center;'>"
                    f"<b>Qualité de l'air : {label}</b></div>",
                    unsafe_allow_html=True
                )

                st.metric("Indice AQI", aqi)
                st.markdown("#### Composants mesurés :")
                for comp, val in components.items():
                    st.write(f"{comp.upper()} : {val} µg/m³")
            else:
                st.warning("❌ Données indisponibles.")
        except Exception as e:
            st.error(f"Erreur AQI : {e}")

        st.subheader("📍 Localisation")
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 13px;'>Made with ❤️ by Yasmine Abdennadher – Été 2025</div>",
        unsafe_allow_html=True
    )
