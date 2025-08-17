import pytest
import pandas as pd
from unittest.mock import patch
from datetime import datetime
from app_modules import ecommerce_utils, nutrition_utils

# ---------- 🧪 TESTS ECOMMERCE ---------- #

def test_preprocess_ecommerce_data():
    # Simuler un DataFrame e-commerce simple
    data = {
        "InvoiceDate": [datetime(2010, 12, 1), datetime(2011, 1, 1)],
        "Quantity": [10, 5],
        "UnitPrice": [2.5, 3.0]
    }
    df = pd.DataFrame(data)
    result = ecommerce_utils.preprocess_ecommerce_data(df)
    
    assert "TotalAmount" in result.columns
    assert result["TotalAmount"].iloc[0] == 25.0

def test_generate_prophet_forecast():
    # Simuler un DataFrame agrégé sur les ventes journalières
    data = {
        "ds": pd.date_range(start="2022-01-01", periods=10),
        "y": [100, 120, 130, 90, 110, 105, 98, 115, 123, 134]
    }
    df = pd.DataFrame(data)
    forecast, model = ecommerce_utils.generate_prophet_forecast(df)
    
    assert "ds" in forecast.columns
    assert "yhat" in forecast.columns
    assert len(forecast) > 0

