# openfoodfacts_connector.py

import requests
import pandas as pd
from typing import Union, Optional

BASE_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"
BASE_PRODUCT_URL = "https://world.openfoodfacts.org/api/v0/product/"

HEADERS = {"User-Agent": "PredictiveAnalyticsStage/1.0"}

def search_products(query: str, page_size: int = 5) -> pd.DataFrame:
    """Recherche les produits par nom et retourne un DataFrame structuré."""
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size
    }
    response = requests.get(BASE_SEARCH_URL, headers=HEADERS, params=params)
    response.raise_for_status()

    data = response.json().get("products", [])
    if not data:
        return pd.DataFrame()

    results = []
    for product in data:
        results.append({
            "product_name": product.get("product_name", ""),
            "code": product.get("code", ""),
            "brands": product.get("brands", ""),
            "categories": product.get("categories", ""),
            "countries": product.get("countries", ""),
            "nutrition_grade": product.get("nutrition_grades", ""),
            "image_url": product.get("image_url", "")
        })

    return pd.DataFrame(results)

def get_product_by_barcode(barcode: str) -> Optional[dict]:
    """Récupère un produit par code-barres."""
    url = f"{BASE_PRODUCT_URL}{barcode}.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    product = response.json().get("product")
    if not product:
        return None

    return {
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "categories": product.get("categories", ""),
        "countries": product.get("countries", ""),
        "nutrition_grade": product.get("nutrition_grades", ""),
        "energy_100g": product.get("nutriments", {}).get("energy_100g"),
        "sugars_100g": product.get("nutriments", {}).get("sugars_100g"),
        "salt_100g": product.get("nutriments", {}).get("salt_100g"),
        "image_url": product.get("image_url", "")
    }
