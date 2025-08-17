import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Modules principaux
from meteo_app import run as run_meteo_app
from air_quality_app import run as run_air_app
from churn_app import run as run_churn_app
from sales_app import run as run_sales_app

# Explorateurs
from ecommerce_app import run as run_ecommerce_app
from nutrition_app import run as run_nutrition_app
from covid_app import run as run_covid_app

# 🛠️ Configuration de la page
st.set_page_config(
    page_title="Dashboard IA – Prévision & Analyse",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard IA – Données Prédictives")
st.markdown("""
Bienvenue dans votre **plateforme intelligente** regroupant plusieurs modules :
- 🌤️ Météo & Qualité de l'air
- 👥 Prédiction de churn client
- 🛍️ Prévision de ventes

Et des explorateurs pour d'autres données :
- 📦 Ecommerce
- 🧬 OpenFoodFacts
- 🦠 COVID-19
""")

# 🧭 Menu latéral
st.sidebar.title("🧭 Navigation")
selected_module = st.sidebar.radio(
    "Sélectionnez un module à explorer :",
    options=[
        "🌤️ Météo & Air",
        "👥 Prédiction de churn client",
        "🛍️ Prévision des ventes",
        "📦 Ecommerce",
        "🧬 OpenFoodFacts",
        "🦠 Covid-19"
    ]
)

# 🔀 Modules
if selected_module == "🌤️ Météo & Air":
    sub_module = st.radio(
        "Choisissez une analyse spécifique :",
        ["🌦️ Météo", "🌫️ Qualité de l'air"],
        horizontal=True
    )
    if sub_module == "🌦️ Météo":
        run_meteo_app()
    else:
        run_air_app()

elif selected_module == "👥 Prédiction de churn client":
    run_churn_app()
elif selected_module == "🛍️ Prévision des ventes":
    run_sales_app()
elif selected_module == "📦 Ecommerce":
    run_ecommerce_app()
elif selected_module == "🧬 OpenFoodFacts":
    run_nutrition_app()
elif selected_module == "🦠 Covid-19":
    run_covid_app()
