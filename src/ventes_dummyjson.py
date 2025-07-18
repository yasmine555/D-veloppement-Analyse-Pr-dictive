import requests
import pandas as pd
from datetime import datetime, timedelta

def get_sales_data_from_api():
    url = "https://dummyjson.com/carts"
    all_sales = []

    for page in range(1, 6):  # 5 pages pour simuler plus d'historique
        response = requests.get(f"{url}?limit=20&skip={(page-1)*20}")
        data = response.json()
        for cart in data['carts']:
            # Simulation de date à rebours depuis aujourd’hui
            fake_date = datetime.today() - timedelta(days=cart['id'])
            all_sales.append({
                "date": fake_date.strftime('%Y-%m-%d'),
                "total": cart['total'],
                "discounted_total": cart['discountedTotal'],
                "total_products": cart['totalProducts'],
                "total_quantity": cart['totalQuantity']
            })

    df = pd.DataFrame(all_sales)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values("date").reset_index(drop=True)
    return df
