# chatbot/model_gateway.py
from typing import Dict, Any

# ⚠️ ADAPTE CES IMPORTS à ton projet réel
# Exemple si tu as src/sales_model.py avec une fonction predict_sales(data: dict) -> float
try:
    from src.sales_model import predict_sales as _predict_sales
except Exception:
    _predict_sales = None

try:
    from src.churn_model import predict_churn as _predict_churn
except Exception:
    _predict_churn = None

# TODO: ajoute ici les autres modèles (météo, air, covid, nutrition, ecommerce)
# from src.weather_model import predict_weather as _predict_weather
# ...

def available_models() -> Dict[str, bool]:
    return {
        "sales": _predict_sales is not None,
        "churn": _predict_churn is not None,
        # "weather": _predict_weather is not None,
        # ...
    }

def predict_via_gateway(intent: str, data: Dict[str, Any]):
    intent = intent.lower().strip()
    if intent in ("sales", "ventes"):
        if _predict_sales is None:
            return {"error": "Le modèle Ventes n'est pas importable dans ce contexte."}
        return {"prediction": _predict_sales(data)}

    if intent == "churn":
        if _predict_churn is None:
            return {"error": "Le modèle Churn n'est pas importable dans ce contexte."}
        return {"prediction": _predict_churn(data)}

    return {"error": f"Modèle '{intent}' non reconnu ou non branché."}
