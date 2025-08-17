# app/api/app.py
import os
import joblib
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "../../models/latest_model.joblib")

app = Flask(__name__)

def load_model(path=MODEL_PATH):
    model_bundle = joblib.load(path) 
    return model_bundle

model_bundle = None

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    global model_bundle
    if model_bundle is None:
        model_bundle = load_model()

    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON body found"}), 400

    # Support single or batch predictions
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    try:
        X = model_bundle["preprocessor"].transform(df)
        preds = model_bundle["model"].predict_proba(X)[:, 1].tolist()
        return jsonify({"predictions": preds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
