import pandas as pd
import joblib
import os

# Charger le modèle
model_path = os.path.join(os.path.dirname(__file__), "model_churn_xgb.pkl")
model = joblib.load(model_path)

# ✅ Les colonnes que le modèle attend (copiées depuis les données d'entraînement)
expected_columns = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaperlessBilling_Yes',
    'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check'
]

def preprocess(df):
    df = df.copy()

    # Nettoyage
    df = df[df['TotalCharges'] != ' ']
    df['TotalCharges'] = df['TotalCharges'].astype(float)
    df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)

    # Encodage booléens : ne surtout pas les mapper à 1/0
    # get_dummies s'en charge (sinon tu perds "Partner_Yes")
    
    # Supprimer customerID si présent
    if 'customerID' in df.columns:
        df.drop('customerID', axis=1, inplace=True)

    # Encodage one-hot
    df_encoded = pd.get_dummies(df, drop_first=False)

    # Ajouter colonnes manquantes
    for col in expected_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Réordonner
    df_encoded = df_encoded[expected_columns]

    return df_encoded

def predict_from_df(df):
    df_prepared = preprocess(df)
    predictions = model.predict(df_prepared)
    return pd.Series(predictions)
