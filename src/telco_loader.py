import pandas as pd

def load_telco_dataset(filepath):
    """
    Charge et nettoie le dataset Telco Customer Churn.
    - Convertit les colonnes booléennes
    - Gère les valeurs manquantes
    """
    df = pd.read_csv(filepath)

    # Nettoyage
    df.columns = df.columns.str.strip()
    df = df[df['TotalCharges'] != ' ']
    df['TotalCharges'] = df['TotalCharges'].astype(float)

    # Conversion des colonnes booléennes
    bool_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in bool_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    return df
