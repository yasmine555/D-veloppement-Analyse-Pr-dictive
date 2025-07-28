# app_streamlit/sales_app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

def run():
    st.set_page_config(page_title="Prévision de Ventes", layout="centered")
    st.title("📈 Prévision de Ventes")

    MODEL_PATH = os.path.join(os.path.dirname(__file__), '../app_streamlit/models/sales_model.pkl')

    @st.cache_resource
    def load_model():
        return joblib.load(MODEL_PATH)

    model = load_model()

    # Date future
    date_input = st.date_input("Choisissez une date pour la prédiction")

    if st.button("Prévoir les ventes"):
        today = datetime.today().date()
        delta_days = (date_input - today).days

        t = np.array([[delta_days]])
        prediction = model.predict(t)

        st.success(f"Prévision des ventes pour le {date_input}: **{prediction[0]:.2f}** unités.")
