from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)
MODEL_PATH = "models/model_churn_xgb.pkl"

# Charger le modèle une seule fois
model = joblib.load(MODEL_PATH)

def preprocess_data(df):
    df = df[df["TotalCharges"] != " "]
    df["TotalCharges"] = df["TotalCharges"].astype(float)
    if "customerID" in df.columns:
        df.drop(["customerID"], axis=1, inplace=True)
    df = pd.get_dummies(df, drop_first=True)

    # Ajustement des colonnes attendues
    model_features = model.get_booster().feature_names
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]

    return df

@app.route("/")
def home():
    return "🚀 API de prédiction de churn opérationnelle !"

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé."}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file)
        df_prepared = preprocess_data(df)
        preds = model.predict(df_prepared)
        results = df.copy()
        results["Churn_Prediction"] = preds
        return results[["Churn_Prediction"]].to_json(orient="records")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict/json", methods=["POST"])
def predict_from_json():
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "Aucune donnée JSON reçue."}), 400

        df = pd.DataFrame(input_data)
        df_prepared = preprocess_data(df)
        preds = model.predict(df_prepared)
        return jsonify({"predictions": preds.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
