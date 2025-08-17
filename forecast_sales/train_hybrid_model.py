# forecast_sales/train_hybrid_model.py
import os
import joblib
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'app_streamlit', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def get_sales_data_from_api():
    url = "https://raw.githubusercontent.com/selva86/datasets/master/a10.csv"
    df = pd.read_csv(url, parse_dates=['date'])
    df = df.rename(columns={'value': 'y'})
    df = df.sort_values('date').reset_index(drop=True)
    return df

def train_hybrid():
    print("📥 Chargement des données...")
    df = get_sales_data_from_api()
    df['ds'] = df['date']

    print("🔮 Entraînement Prophet (tendance)...")
    prophet = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    prophet.fit(df[['ds', 'y']])

    print("🔁 Prédiction Prophet sur historique pour récupérer yhat...")
    forecast_hist = prophet.predict(df[['ds']])
    df['yhat_prophet'] = forecast_hist['yhat'].values

    print("📉 Calcul des résidus (y - yhat_prophet)...")
    df['residual'] = df['y'] - df['yhat_prophet']

    print("⚙️ Création des features temporelles pour le modèle sur résidus...")
    df['day'] = df['ds'].dt.day
    df['month'] = df['ds'].dt.month
    df['year'] = df['ds'].dt.year
    df['dayofweek'] = df['ds'].dt.dayofweek
    features = ['day', 'month', 'year', 'dayofweek']

    X = df[features]
    y_res = df['residual']

    print("🌲 Entraînement RandomForest sur les résidus...")
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X, y_res)

    print("🧪 Évaluation hybride sur historique...")
    resid_pred = rf.predict(X)
    hybrid_pred = df['yhat_prophet'] + resid_pred
    rmse = np.sqrt(mean_squared_error(df['y'], hybrid_pred))  # pas d'argument `squared` pour compatibilité
    print(f"✅ RMSE hybride (historique) : {rmse:.4f}")

    # Sauvegarder les modèles séparément
    prophet_path = os.path.join(MODEL_DIR, "prophet_model.pkl")
    rf_path = os.path.join(MODEL_DIR, "residual_rf_model.pkl")
    joblib.dump(prophet, prophet_path)
    joblib.dump(rf, rf_path)
    print(f"💾 Modèles sauvegardés :\n - {prophet_path}\n - {rf_path}")

if __name__ == "__main__":
    train_hybrid()
