# 📁 src/nutrition_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.set_page_config(page_title="Nutrition Analyzer", layout="wide")

    st.title("🍎 Nutrition Clustering App")
    st.write("Explorez les données nutritionnelles avec clustering, visualisations et NutriScore.")

    uploaded_file = st.file_uploader("📂 Upload ton fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Aperçu brut
        st.subheader("🔍 Aperçu brut des données")
        st.dataframe(df.head())

        # Nettoyage
        cols = ['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs', 'Grams']
        df.replace("t", pd.NA, inplace=True)
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df_clean = df.dropna(subset=cols).copy()

        # Catégories
        categories = df_clean['Category'].unique()
        selected_categories = st.multiselect("🗂️ Filtrer par catégories", categories, default=list(categories))
        df_clean = df_clean[df_clean['Category'].isin(selected_categories)]

        # Clustering
        st.sidebar.header("⚙️ Paramètres Clustering")
        k = st.sidebar.slider("Nombre de clusters (KMeans)", 2, 10, 3)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_clean[cols])
        kmeans = KMeans(n_clusters=k, random_state=42)
        df_clean["Cluster"] = kmeans.fit_predict(X_scaled)

        # NutriScore
        def compute_nutriscore(row):
            score = 0
            if row["Calories"] > 500: score += 2
            if row["Fat"] > 20: score += 2
            if row["Sat.Fat"] > 10: score += 1
            if row["Fiber"] >= 3: score -= 1
            if row["Protein"] >= 10: score -= 1
            return score

        df_clean["NutriScore"] = df_clean.apply(compute_nutriscore, axis=1)
        df_clean["NutriScore"] = pd.cut(
            df_clean["NutriScore"],
            bins=[-np.inf, 0, 2, 4, 6, np.inf],
            labels=["A", "B", "C", "D", "E"]
        )

        # Résultats
        st.subheader("📊 Données enrichies avec Cluster et NutriScore")
        st.dataframe(df_clean[["Food", "Category", "Calories", "Protein", "Fat", "Fiber", "Cluster", "NutriScore"]].head(10))

        # Visualisations
        st.subheader("📈 Visualisations")
        tab1, tab2, tab3, tab4 = st.tabs(["Histogrammes", "Boxplots", "Corrélations", "Scatter"])

        with tab1:
            col = st.selectbox("Variable pour histogramme", cols)
            fig, ax = plt.subplots()
            sns.histplot(data=df_clean, x=col, hue="Cluster", multiple="stack", ax=ax)
            st.pyplot(fig)

        with tab2:
            col = st.selectbox("Variable pour boxplot", cols, key="box")
            fig2, ax2 = plt.subplots()
            sns.boxplot(data=df_clean, x="Cluster", y=col, ax=ax2)
            st.pyplot(fig2)

        with tab3:
            fig3, ax3 = plt.subplots(figsize=(8,6))
            sns.heatmap(df_clean[cols].corr(), annot=True, cmap="YlOrRd", ax=ax3)
            st.pyplot(fig3)

        with tab4:
            x_axis = st.selectbox("Axe X", cols, index=1)
            y_axis = st.selectbox("Axe Y", cols, index=2)
            fig4, ax4 = plt.subplots()
            sns.scatterplot(data=df_clean, x=x_axis, y=y_axis, hue="Cluster", palette="tab10", ax=ax4)
            st.pyplot(fig4)

        st.subheader("🅰️ Répartition des NutriScores")
        fig5, ax5 = plt.subplots()
        sns.countplot(data=df_clean, x="NutriScore", order=["A", "B", "C", "D", "E"], palette="Set2", ax=ax5)
        st.pyplot(fig5)

    else:
        st.info("👈 Charge un fichier CSV pour commencer l’analyse.")
