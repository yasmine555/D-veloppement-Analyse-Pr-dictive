# app_streamlit/sales_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import shap
import plotly.graph_objs as go
from pathlib import Path
from datetime import timedelta

MODEL_DIR = Path(__file__).parent / "models"
DATA_URL = "https://raw.githubusercontent.com/selva86/datasets/master/a10.csv"

# --- Chargement ---
@st.cache_resource
def load_models():
    prophet_path = MODEL_DIR / "prophet_model.pkl"
    rf_path = MODEL_DIR / "residual_rf_model.pkl"
    if not prophet_path.exists() or not rf_path.exists():
        st.error(f"Modèles manquants dans {MODEL_DIR}. Exécute train_hybrid_model.py d'abord.")
        st.stop()
    prophet = joblib.load(prophet_path)
    rf = joblib.load(rf_path)
    return prophet, rf

@st.cache_data
def load_history():
    df = pd.read_csv(DATA_URL, parse_dates=['date'])
    df = df.rename(columns={'value': 'y'})
    df = df.sort_values('date').reset_index(drop=True)
    return df

def create_features_for_dates(dates):
    # Convertir en Series pour que .dt fonctionne même si c'est un DatetimeIndex
    if isinstance(dates, pd.DatetimeIndex):
        dates = pd.Series(dates)
    dates = pd.to_datetime(dates)  # sécurité
    return pd.DataFrame({
        "day": dates.dt.day,
        "month": dates.dt.month,
        "year": dates.dt.year,
        "dayofweek": dates.dt.dayofweek
    })



def plot_history_and_forecast(df_hist, df_forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_hist['date'], y=df_hist['y'], mode='lines', name='Historique'))
    fig.add_trace(go.Scatter(x=df_forecast['date'], y=df_forecast['yhat_prophet'], mode='lines',
                             name='Tendance (Prophet)', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df_forecast['date'], y=df_forecast['yhat_hybrid'], mode='lines',
                             name='Prévision hybride (Prophet + RF)', line=dict(color='firebrick')))
    fig.update_layout(title="Historique et prévisions (hybride)", xaxis_title="Date", yaxis_title="Ventes")
    st.plotly_chart(fig, use_container_width=True)

def explain_rf_prediction(rf_model, X_train_background, X_sample):
    """Affiche une explication SHAP (TreeExplainer) pour RandomForest sur X_sample"""
    st.subheader("🔍 Explication (RandomForest sur résidu) — SHAP")
    try:
        explainer = shap.TreeExplainer(rf_model, X_train_background)
        shap_values = explainer.shap_values(X_sample)
        # waterfall pour une seule prédiction
        shap.plots._waterfall.waterfall_legacy(explainer.expected_value, shap_values[0], X_sample.iloc[0], show=False)
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.error(f"Erreur SHAP: {e}")

# --- MAIN RUN PAGE ---
def run():
    st.set_page_config(page_title="Prévision Hybride des Ventes", layout="wide")
    st.title("📈 Prévision Hybride (Prophet + RandomForest) — Vente du rêve ✨")
    st.markdown("Historique + prévision future, avec explication SHAP des résidus.")

    prophet, rf = load_models()
    df_hist = load_history()

    # afficher historique
    st.subheader("Historique des ventes")
    st.write(f"Période : {df_hist['date'].min().date()} → {df_hist['date'].max().date()}")
    st.line_chart(df_hist.set_index('date')['y'])

    # choix horizon
    horizon_days = st.slider("Horizon de prévision (jours)", min_value=30, max_value=365, value=180, step=1)

    # créer dates futures contiguës
    last_date = df_hist['date'].max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon_days, freq='D')

    # 1) Prophet pour la tendance future
    df_future_prophet = pd.DataFrame({'ds': future_dates})
    prophet_forecast = prophet.predict(df_future_prophet)
    yhat_prophet = prophet_forecast['yhat'].values

    # 2) RandomForest pour residus sur les features futures
    X_future = create_features_for_dates(future_dates)
    resid_pred = rf.predict(X_future)

    # 3) Somme = prévision hybride
    yhat_hybrid = yhat_prophet + resid_pred

    # DataFrames de sortie
    df_forecast = pd.DataFrame({
        'date': future_dates,
        'yhat_prophet': yhat_prophet,
        'resid_pred': resid_pred,
        'yhat_hybrid': yhat_hybrid
    })

    # plot interactif (historique + tendances + hybride)
    plot_history_and_forecast(df_hist, df_forecast)

    # Table preview
    with st.expander("Voir les premières prévisions"):
        st.dataframe(df_forecast.head(10))

    # Explication SHAP : on va utiliser comme background X_train (quelques échantillons historiques)
    st.markdown("---")
    st.subheader("Explication d'une prédiction future (choisir un jour)")
    idx = st.slider("Choisir jour futur (index)", 0, len(df_forecast)-1, 0)
    chosen_date = df_forecast.loc[idx, 'date']
    st.write(f"Date choisie : **{pd.Timestamp(chosen_date).date()}**")

    X_sample = create_features_for_dates(pd.to_datetime([chosen_date]))
    # background: prend un échantillon du training (features historiques)
    hist_features = create_features_for_dates(df_hist['date'])
    background = hist_features.sample(min(len(hist_features), 200), random_state=42)

    # Explanation (tree SHAP)
    explain_rf_prediction(rf, background, X_sample)

    st.success("✅ Prédiction et explication générées.")

# rendre disponible quand importé
if __name__ == "__main__":
    run()
