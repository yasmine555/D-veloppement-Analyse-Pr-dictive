import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import subprocess

st.set_page_config(page_title="Dashboard IA", layout="wide")

choice = option_menu(
    menu_title=None,
    options=["Prédiction Churn", "Prévision Ventes"],
    icons=["person-check", "bar-chart"],
    orientation="horizontal",
)

if choice == "Prédiction Churn":
    st.rerun()  # Relance la page churn.py
    subprocess.run(["streamlit", "run", "app_streamlit/churn.py"])
elif choice == "Prévision Ventes":
    st.rerun()
    subprocess.run(["streamlit", "run", "app_streamlit/sales_forecasting.py"])
