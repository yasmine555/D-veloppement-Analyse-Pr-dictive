# 📊 Dashboard IA – Données Prédictives

Ce projet est un tableau de bord Streamlit, intégrant plusieurs modules d’IA pour la prédiction et l’analyse de données.

---

## 🗂️ Structure du projet

projet_stage_ete_2025/
│
├── api/ # API Flask
├── app_streamlit/ # Dashboard Streamlit
├── chatbot/ # Chatbot (nouveau module)
├── src/ # Scripts Python (connecteurs, entraînement modèles)
├── data/ # Jeux de données
├── models/ # Modèles entraînés (.joblib)
├── notebooks/ # Notebooks Jupyter
├── docker-compose.yml # Orchestration Docker
├── requirements.txt # Dépendances
├── .env # Variables sensibles
└── README.md # Ce fichier



---

## ⚙️ Installation locale (sans Docker)

### 1. Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
2. Installer les dépendances

pip install --upgrade pip
pip install -r requirements.txt
🚀 Générer le modèle de prévision
1. Ajouter vos données
Placez votre fichier CSV des ventes dans data/sales_data.csv.

2. Entraîner le modèle

python src/train_model.py
Ce script :

Charge les données

Entraîne un modèle RandomForest

Sauvegarde models/latest_model.joblib

▶️ Lancer en local (sans Docker)
Dashboard Streamlit

cd app_streamlit
streamlit run main.py
API Flask

cd api
python main.py
🐳 Lancer avec Docker
1. Construire et lancer tous les services
Depuis la racine :

bash

docker-compose up --build
Services démarrés :

API Flask : http://localhost:8000

Streamlit : http://localhost:8501

Chatbot : http://localhost:8600

2. Arrêter les services
bash

docker-compose down
📌 Avantages :

Aucun besoin d’installer Python localement

Même environnement pour tous les développeurs

📌 Modules disponibles
 Météo |  Qualité de l’air |  Churn client | Prévision ventes
+ nutirion + covid + ecommerce

✨ Auteur
Yasmine Abdennadher – Ingénieure en Data Science & IA
Stage chez YottaByte – Été 2025