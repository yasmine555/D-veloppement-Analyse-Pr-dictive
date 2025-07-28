import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Charger les données
df = pd.read_csv("data/produits_ecommerce.csv")

# Encodage des variables catégorielles
for col in ['brand', 'category']:
    df[col] = LabelEncoder().fit_transform(df[col])

# Simuler une variable "ventes estimées" à partir du stock (plus le stock est faible, plus les ventes ont été élevées)
df['ventes_estimees'] = df['stock'].max() - df['stock']

# Sélection des features
X = df[['price', 'rating', 'brand', 'category']]
y = df['ventes_estimees']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modèle XGBoost
model = XGBRegressor()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print(f"✅ RMSE du modèle : {rmse:.2f}")
