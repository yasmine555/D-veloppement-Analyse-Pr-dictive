from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/sales_model.pkl')
model = joblib.load(MODEL_PATH)

@app.route('/predict_sales', methods=['GET'])
def predict_sales():
    # Date attendue en paramètre 'date' au format YYYY-MM-DD
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': "Paramètre 'date' manquant"}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': "Format de date invalide. Utiliser YYYY-MM-DD"}), 400

    today = datetime.today()
    delta_days = (date_obj - today).days
    if delta_days < 0:
        return jsonify({'error': "Date doit être aujourd'hui ou dans le futur"}), 400

    t = np.array([[delta_days]])
    prediction = model.predict(t)[0]

    return jsonify({
        'date': date_str,
        'predicted_sales': float(prediction)
    })

if __name__ == '__main__':
    app.run(debug=True)
