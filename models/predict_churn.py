import pandas as pd
import joblib
import os

MODEL_PATH = "models/model_churn_xgb.pkl"

# Charger le modèle sauvegardé
model = joblib.load(MODEL_PATH)

# Fonction de préparation des données
def preprocess_input(df):
    df = df.copy()
    df = df[df["TotalCharges"] != " "]
    df["TotalCharges"] = df["TotalCharges"].astype(float)
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)
    df = pd.get_dummies(df, drop_first=True)

    # S'assurer que les colonnes du modèle sont bien présentes
    model_features = model.get_booster().feature_names
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]

    return df

# Fonction principale de prédiction

def predict_from_df(df_raw):
    try:
        df = df_raw.copy()
        df["__index"] = range(len(df))  # Sauvegarder l'index

        # Filtrer les lignes valides
        df_valid = df[df["TotalCharges"] != " "].copy()
        df_valid["TotalCharges"] = df_valid["TotalCharges"].astype(float)

        if "customerID" in df_valid.columns:
            df_valid.drop("customerID", axis=1, inplace=True)

        df_valid = pd.get_dummies(df_valid, drop_first=True)

        model_features = model.get_booster().feature_names
        for col in model_features:
            if col not in df_valid.columns:
                df_valid[col] = 0
        df_valid = df_valid[model_features]

        # Prédictions sur les lignes valides
        preds = model.predict(df_valid)

        # Reconstruire une colonne avec tous les indices
        full_preds = pd.Series([None] * len(df), index=df["__index"])
        full_preds.loc[df_valid.index] = preds

        return full_preds

    except Exception as e:
        raise ValueError(f"Erreur pendant la prédiction : {str(e)}")
