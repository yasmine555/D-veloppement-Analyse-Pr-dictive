import os
import sys
import pandas as pd

# 🧭 Ajouter le chemin vers le dossier src/
sys.path.append(os.path.abspath("src"))

# 📥 Importer la fonction
from models.predict_churn import predict_from_df

# 📊 Charger un échantillon du dataset
df = pd.read_csv("data/WA_Fn_UseC_Telco_Customer_Churn.csv")
df_sample = df.sample(5, random_state=42)

# 🔮 Prédire
results = predict_from_df(df_sample)

print("✅ Prédictions :", results)
