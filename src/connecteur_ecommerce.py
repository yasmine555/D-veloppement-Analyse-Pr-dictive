import requests
import pandas as pd

def fetch_products():
    url = "https://dummyjson.com/products?limit=100"
    response = requests.get(url)
    data = response.json()
    products = data['products']
    return pd.DataFrame(products)

if __name__ == "__main__":
    df_products = fetch_products()
    df_products.to_csv("data/produits_ecommerce.csv", index=False)
    print("✅ Données produits e-commerce récupérées avec succès.")
