# 📁 app_streamlit/weather_app.py
import streamlit as st
from meteo_app import run_meteo
from air_quality_app import run_air_quality

def run():
    st.title("🌤️ Météo & Qualité de l'air")

    option = st.radio("Sélectionnez une sous-section :", ["📡 Météo", "💨 Qualité de l'air"])

    if option == "📡 Météo":
        run_meteo()
    elif option == "💨 Qualité de l'air":
        run_air_quality()
