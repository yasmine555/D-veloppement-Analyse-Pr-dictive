import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/sales_model.pkl')

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.set_page_config(page_title="Prévision de Ventes", layout="centered")
st.title("📈 Prévision de Ventes")

model = load_model()

# Saisie date future pour prédiction
date_input = st.date_input("Choisissez une date pour la prédiction")

if st.button("Prévoir les ventes"):

    # Convertir date en feature numérique 't'
    today = datetime.today()
    delta_days = (date_input - today).days
    t = np.array([[len(range(delta_days)) + delta_days]])  # Ou juste un entier croissant simple

    # Prédiction
    prediction = model.predict(t)

    st.write(f"Prévision des ventes pour le {date_input}: **{prediction[0]:.2f}** unités.")
