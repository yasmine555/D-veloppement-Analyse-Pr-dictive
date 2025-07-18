import streamlit as st
import pandas as pd
import os
import sys
import joblib
import plotly.express as px

# Ajouter src/ au path pour importer predict_from_df
sys.path.append(os.path.abspath("src"))
from models.predict_churn import predict_from_df

st.set_page_config(page_title="Prédiction Churn Clients", layout="centered")
st.title("🔮 Prédiction de Churn – Telco")

uploaded_file = st.file_uploader("📤 Importez un fichier CSV avec les données clients", type="csv")

if uploaded_file:
    try:
        df_input = pd.read_csv(uploaded_file)
        st.subheader("📋 Aperçu des données :")
        st.dataframe(df_input.head())

        # Prédiction
        predictions = predict_from_df(df_input)
        df_input["Prédiction"] = predictions.values

        st.subheader("🔎 Résultats de la prédiction :")
        st.write("🟢 0 = Client fidèle &nbsp;&nbsp;&nbsp;&nbsp; 🔴 1 = Risque de churn")

        st.dataframe(df_input[["Prédiction"]])

        # 📊 Visualisation avec Plotly
        st.subheader("📊 Visualisation des résultats")
        fig = px.histogram(df_input, x="Prédiction", color="Prédiction", barmode="group",
                           title="Distribution des prédictions",
                           labels={"Prédiction": "Churn (1) / Fidèle (0)"},
                           color_discrete_map={0: "green", 1: "red"})
        st.plotly_chart(fig)

        # 📥 Option de téléchargement
        csv = df_input.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les résultats",
            data=csv,
            file_name="churn_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
else:
    st.info("👉 Veuillez importer un fichier CSV pour commencer.")
