# 📁 main.py

import streamlit as st
import sys
import os

# Ajouter src/ au chemin système si besoin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


# 🔌 Import des modules locaux
from weather_app import run as run_weather_air_app
from churn_app import run as run_churn_app
from sales_app import run as run_sales_app

# 🛠️ Configuration de la page
st.set_page_config(
    page_title="Dashboard IA – Prévision & Analyse",
    page_icon="📊",
    layout="wide"
)

# 🧠 Titre principal
st.title("📊 Dashboard IA – Données Prédictives")
st.markdown("""
Bienvenue dans votre **plateforme intelligente** regroupant plusieurs modules :
- 🌤️ Météo & Qualité de l'air
- 👥 Prédiction de churn client
- 🛍️ Prévision de ventes

Utilisez le menu à gauche pour naviguer entre les modules.
""")

# 🧭 Menu de navigation
st.sidebar.title("🧭 Navigation")
selected_module = st.sidebar.radio(
    "Sélectionnez un module à explorer :",
    options=[
        "🌤️ Météo & Air",
        "👥 Prédiction de churn client",
        "🛍️ Prévision des ventes"
    ]
)

# 🔀 Lancement dynamique du module sélectionné
if selected_module == "🌤️ Météo & Air":
    run_weather_air_app()

elif selected_module == "👥 Prédiction de churn client":
    run_churn_app()

elif selected_module == "🛍️ Prévision des ventes":
    run_sales_app()

else:
    st.warning("⚠️ Veuillez sélectionner un module.")
