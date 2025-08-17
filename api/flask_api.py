from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../app_streamlit/models/sales_model.pkl')
model_bundle = joblib.load(MODEL_PATH)
prophet_model = model_bundle['prophet']
linear_model = model_bundle['linear']
last_t = model_bundle['last_t']

app = Flask(__name__)

@app.route('/predict_sales', methods=['GET'])
def predict_sales():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': "Paramètre 'date' manquant"}), 400

    try:
        date_obj = pd.to_datetime(date_str)
    except ValueError:
        return jsonify({'error': "Format de date invalide. Utiliser YYYY-MM-DD"}), 400

    # Calcul de t (décalage par rapport à la dernière observation)
    months_diff = (date_obj.year - 1991) * 12 + date_obj.month - 7  # basé sur dataset a10
    t_value = months_diff

    # Prédiction Prophet
    future_df = pd.DataFrame({'ds': [date_obj]})
    prophet_pred = prophet_model.predict(future_df)['yhat'].iloc[0]

    # Prédiction finale avec LinearRegression
    X_new = np.array([[t_value, prophet_pred]])
    prediction = linear_model.predict(X_new)[0]

    return jsonify({
        'date': date_str,
        'predicted_sales': float(prediction)
    })

if __name__ == '__main__':
    app.run(debug=True)