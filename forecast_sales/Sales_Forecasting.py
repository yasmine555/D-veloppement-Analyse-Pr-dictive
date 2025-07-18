# sales_forecasting.py

import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import os

import json  

def get_sales_data_from_api():
    """Extrait les données de ventes depuis un fichier JSON brut sur GitHub."""
    response = requests.get("https://raw.githubusercontent.com/selva86/datasets/master/a10.json")
    data = response.json()  # ✅ plus fiable
    df = pd.DataFrame(data["data"], columns=["date", "value"])
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    return df



def create_features(df):
    """Crée des variables explicatives simples à partir de la date."""
    df['t'] = np.arange(len(df))
    return df[['t']], df['value']

def train_forecast_model(X, y):
    """Entraîne un modèle simple de régression linéaire pour la prévision."""
    model = LinearRegression()
    model.fit(X, y)
    return model

def save_model(model, path='models/sales_model.pkl'):
    """Sauvegarde le modèle entraîné."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(path='models/sales_model.pkl'):
    """Charge un modèle existant."""
    return joblib.load(path)

if __name__ == "__main__":
    df = get_sales_data_from_api()
    X, y = create_features(df)
    model = train_forecast_model(X, y)
    save_model(model)
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    print(f"✅ Modèle entraîné et sauvegardé avec RMSE: {rmse:.2f}")
