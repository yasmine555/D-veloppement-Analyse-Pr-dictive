import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly
import os

# Chargement des données depuis un fichier local
@st.cache_data
def load_data():
    path = "data/produits_ecommerce.csv"
    if not os.path.exists(path):
        st.error("❌ Fichier 'produits_ecommerce.csv' introuvable. Veuillez exécuter le script de récupération.")
        st.stop()
    df = pd.read_csv(path)
    return df

# Application principale
def run():
    st.set_page_config(page_title="📦 Dashboard E-Commerce", layout="wide")
    st.title("📊 Dashboard E-commerce Intelligent")
    
    section = st.sidebar.radio(
        "Menu",
        ["🛒 Analyse Produits", "💰 Analyse Ventes", "👥 Analyse Clients", "📈 Prévision Ventes"],
        index=0
    )

    df = load_data()

    if section == "🛒 Analyse Produits":
        afficher_analyse_produits(df)
    elif section == "💰 Analyse Ventes":
        afficher_analyse_ventes(df)
    elif section == "👥 Analyse Clients":
        afficher_analyse_clients(df)
    elif section == "📈 Prévision Ventes":
        afficher_prevision_ventes(df)

# ==== Sous-sections ====

def afficher_analyse_produits(df):
    st.subheader("📦 Répartition des Produits par Catégorie")

    categorie_counts = df["category"].value_counts().reset_index()
    categorie_counts.columns = ["Catégorie", "Nombre de produits"]

    fig = px.bar(categorie_counts, x="Catégorie", y="Nombre de produits", color="Catégorie",
                 title="Produits par Catégorie")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**{len(df)}** produits au total.")

def afficher_analyse_ventes(df):
    st.subheader("💰 Analyse Simulée des Ventes (par Date fictive)")

    # Création d'une date aléatoire fictive pour chaque produit
    df['date'] = pd.date_range(start="2024-01-01", periods=len(df), freq="D")
    df['prix_total'] = df['price'] * df['stock']  # simulation de CA potentiel

    df_agg = df.groupby(pd.Grouper(key="date", freq="M"))['prix_total'].sum().reset_index()

    fig = px.line(df_agg, x="date", y="prix_total", markers=True,
                  title="Évolution mensuelle du Chiffre d'Affaires simulé")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_agg.tail(), use_container_width=True)

def afficher_analyse_clients(df):
    st.subheader("👥 Analyse simulée des Clients par Segment")

    # Simulation simple
    segments = ["Nouveaux", "Récurrents", "VIP"]
    counts = [len(df) * 0.6, len(df) * 0.3, len(df) * 0.1]

    df_clients = pd.DataFrame({
        "Segment client": segments,
        "Nombre de clients": counts
    })

    fig = px.pie(df_clients, names="Segment client", values="Nombre de clients", title="Répartition des Clients")
    st.plotly_chart(fig, use_container_width=True)

def afficher_prevision_ventes(df):
    st.subheader("📈 Prévision de Ventes (avec Prophet)")

    # Simulation temporelle comme dans section ventes
    df['date'] = pd.date_range(start="2024-01-01", periods=len(df), freq="D")
    df['prix_total'] = df['price'] * df['stock']
    df_agg = df.groupby(pd.Grouper(key="date", freq="D"))['prix_total'].sum().reset_index()
    df_agg = df_agg.rename(columns={"date": "ds", "prix_total": "y"})

    model = Prophet()
    model.fit(df_agg)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    st.markdown("### 🔮 Prévision des ventes pour les 30 prochains jours")

    fig1 = plot_plotly(model, forecast)
    st.plotly_chart(fig1, use_container_width=True)

    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(), use_container_width=True)

# Lancement
if __name__ == "__main__":
    run()
