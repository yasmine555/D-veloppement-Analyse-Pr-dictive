# src/air_quality_connector.py

import os
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Chargement des variables d'environnement
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_air_quality(lat: float, lon: float) -> dict:
    """
    Récupère les données de qualité de l'air à partir des coordonnées.
    
    Args:
        lat (float): Latitude de la ville
        lon (float): Longitude de la ville

    Returns:
        dict: Données de qualité de l'air (AQI, CO, NO2, etc.)
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/air_pollution?"
        f"lat={lat}&lon={lon}&appid={API_KEY}"
    )

    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def format_air_quality_data(json_data: dict) -> pd.DataFrame:
    """
    Formate les données brutes en DataFrame exploitable.

    Args:
        json_data (dict): Données JSON retournées par l'API

    Returns:
        pd.DataFrame: Données formatées
    """
    records = []
    for item in json_data.get("list", []):
        main = item.get("main", {})
        components = item.get("components", {})
        dt = datetime.utcfromtimestamp(item["dt"]).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "datetime": dt,
            "aqi": main.get("aqi"),
            "co": components.get("co"),
            "no": components.get("no"),
            "no2": components.get("no2"),
            "o3": components.get("o3"),
            "so2": components.get("so2"),
            "pm2_5": components.get("pm2_5"),
            "pm10": components.get("pm10"),
            "nh3": components.get("nh3"),
        }
        records.append(data)

    return pd.DataFrame(records)

def fetch_air_quality(lat: float, lon: float, save_path: str = None) -> pd.DataFrame:
    """
    Fonction principale pour récupérer et sauvegarder les données de qualité de l'air.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        save_path (str, optional): Chemin de sauvegarde en CSV

    Returns:
        pd.DataFrame: Données de qualité de l'air
    """
    print(f"📡 Récupération des données pour ({lat}, {lon})...")
    raw_data = get_air_quality(lat, lon)
    df = format_air_quality_data(raw_data)
    
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"✅ Données sauvegardées sous {save_path}")
    
    return df
