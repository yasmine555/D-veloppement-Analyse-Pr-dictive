# src/covid_app.py

import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA


def run():
    st.set_page_config(page_title="🦠 COVID-19 ARIMA Dashboard", layout="wide")
    st.title("🦠 Prévisions COVID-19 avec ARIMA")

    API_BASE = "https://disease.sh/v3/covid-19/historical"

    @st.cache_data(ttl=3600)
    def fetch_covid_data(country):
        url = f"{API_BASE}/{country}?lastdays=all"
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("timeline", {})
        return {}

    def prepare_series(timeline, var):
        df = pd.DataFrame.from_dict(timeline[var], orient="index", columns=["value"])
        df.index = pd.to_datetime(df.index, format="%m/%d/%y")
        df = df.sort_index()
        df["value"] = df["value"].diff().fillna(0)
        df = df[df["value"] >= 0]
        return df

    countries = ["France", "Germany", "Italy", "United States", "Brazil", "India", "Tunisia", "Morocco"]
    selected_country = st.selectbox("🌍 Choisissez un pays :", countries)
    var_type = st.radio("📌 Type de données :", ["cases", "deaths"], horizontal=True)

    timeline = fetch_covid_data(selected_country)
    if timeline:
        data = prepare_series(timeline, var_type)

        st.subheader(f"📈 Série temporelle des {var_type} quotidiens - {selected_country}")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(x=data.index, y=data.value, name="Historique", mode="lines+markers"))
        st.plotly_chart(fig_hist, use_container_width=True)

        st.subheader("🔮 Prévision avec ARIMA")
        try:
            model = ARIMA(data.value, order=(3, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.get_forecast(steps=5)
            pred = forecast.predicted_mean
            conf_int = forecast.conf_int()

            future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=5)

            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=data.index, y=data.value, name="Historique"))
            fig_forecast.add_trace(go.Scatter(x=future_dates, y=pred, name="Prévision"))
            fig_forecast.add_trace(go.Scatter(x=future_dates, y=conf_int.iloc[:, 0], name="Min", line=dict(dash="dot")))
            fig_forecast.add_trace(go.Scatter(x=future_dates, y=conf_int.iloc[:, 1], name="Max", line=dict(dash="dot")))

            fig_forecast.update_layout(
                title="Prévision ARIMA (5 jours)",
                xaxis_title="Date",
                yaxis_title=var_type.capitalize()
            )
            st.plotly_chart(fig_forecast, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur ARIMA : {e}")
    else:
        st.warning("❌ Impossible de charger les données depuis l'API.")
