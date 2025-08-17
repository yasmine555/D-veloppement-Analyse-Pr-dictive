import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import requests
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from weather_connector import get_weather_forecast

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_coordinates(city, api_key):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        return data['lat'], data['lon']
    else:
        return None, None

def run():
    st.title("📡 Météo – Prévisions à 5 jours")

    city = st.text_input("Entrez le nom d'une ville", "Tunis")

    if not city:
        st.info("Veuillez entrer le nom d'une ville.")
        return

    lat, lon = get_coordinates(city, API_KEY)

    if lat is None or lon is None:
        st.warning("⚠️ Ville introuvable. Vérifiez l'orthographe.")
        return

    st.success(f"Coordonnées de {city} : {lat}, {lon}")

    try:
        data = get_weather_forecast(city)
        df = pd.DataFrame(data)

        st.subheader(f"📊 Prévisions météo pour {city}")
        st.success("Prévisions pour les 5 jours à venir")

        fig_temp = px.line(df, x="datetime", y="temp", title="🌡️ Température")
        st.plotly_chart(fig_temp, use_container_width=True)

        fig_humidity = px.line(df, x="datetime", y="humidity", title="💧 Humidité")
        st.plotly_chart(fig_humidity, use_container_width=True)

        st.markdown("### 🌥️ Description météo")
        st.dataframe(df[["datetime", "description"]].head(10))

    except Exception as e:
        st.error(f"Erreur météo : {e}")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 13px;'>Made with ❤️ by Yasmine Abdennadher – Été 2025</div>",
        unsafe_allow_html=True
    )
