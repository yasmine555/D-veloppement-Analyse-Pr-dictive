import requests
import json

# Charger les données JSON depuis le fichier
with open("exemple_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# URL de ton API Flask
url = "http://127.0.0.1:5000/predict/json"

# Envoyer la requête POST
response = requests.post(url, json=data)

# Afficher la réponse
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
