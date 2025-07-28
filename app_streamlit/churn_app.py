# app_streamlit/churn_app.py

import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px

# Ajouter app_streamlit au path pour importer models
sys.path.append(os.path.dirname(__file__))

from models.predict_churn import predict_from_df

def run():
    st.set_page_config(page_title="🔮 Prédiction Churn Clients", layout="centered")
    st.title("🔮 Prédiction de Churn – Telco")

    uploaded_file = st.file_uploader("📤 Importez un fichier CSV avec les données clients", type="csv")

    if uploaded_file:
        try:
            df_input = pd.read_csv(uploaded_file)
            st.subheader("📋 Aperçu des données :")
            st.dataframe(df_input.head())

            # Prédiction
            predictions = predict_from_df(df_input)
            df_input["Prédiction"] = predictions.map({1: "🔴 Churn", 0: "🟢 Reste"})

            st.subheader("🔎 Résultats de la prédiction :")
            st.dataframe(df_input[["Prédiction"]])

            # 📊 Visualisation avec Plotly
            st.subheader("📊 Visualisation des résultats")
            fig = px.histogram(df_input, x="Prédiction", color="Prédiction",
                               barmode="group",
                               title="Distribution des prédictions",
                               color_discrete_map={"🔴 Churn": "red", "🟢 Reste": "green"})
            st.plotly_chart(fig)

            # 📥 Télécharger
            csv = df_input.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les résultats",
                data=csv,
                file_name="churn_predictions.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Erreur pendant la prédiction : {str(e)}")
    else:
        st.info("👉 Veuillez importer un fichier CSV pour commencer.")
