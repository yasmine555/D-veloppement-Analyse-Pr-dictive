📁 Structure du projet

src/ : scripts Python (ex : connecteurs API)

data/ : jeux de données bruts ou traités

notebooks/ : notebooks Jupyter de test ou modélisation

streamlit_app/ : applications Streamlit (churn et prévision)

forecast_api/ : API Flask pour la prévision de ventes

models/ : modèles entraînés et sauvegardés (.pkl)

docs/ : documentation du projet, bilans hebdomadaires, veille technologique, cas d’usage

.env : variables sensibles (ex : clés API)

requirements.txt : bibliothèques nécessaires

README.md : description globale du projet

🚀 Installation

Cloner le dépôt :

git clone https://github.com/ton-utilisateur/nom-du-depot.git
cd nom-du-depot

Créer et activer un environnement virtuel :

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

Installer les dépendances :

pip install --upgrade pip
pip install -r requirements.txt

🛠️ Usage

1️⃣ Entraînement et génération du modèle de prévision

python src/sales_forecasting.py

Lance le téléchargement des données

Entraîne le modèle de régression linéaire

Sauvegarde le modèle dans models/sales_model.pkl

2️⃣ Lancer l'application Streamlit

streamlit run streamlit_app/main.py

Choix entre :

Prédiction de churn clients

Prévision de ventes

3️⃣ Lancer l'API Flask pour la prévision

cd forecast_api
python predict.py

Endpoint disponible : GET /predict_sales?date=YYYY-MM-DD

Exemple :

curl "http://127.0.0.1:5000/predict_sales?date=2025-07-25"

🔍 Tests fonctionnels

Un script de test rapide est disponible :

bash test_all.sh

(à créer si nécessaire)

📄 Documentation et rapports

Toutes les documentations détaillées, bilans quotidiens et hebdomadaires se trouvent dans docs/ :

docs/bilan_semaine1.md

docs/bilan_semaine2.md

...


# 📊 Dashboard IA – Données Prédictives

Ce projet est un tableau de bord Streamlit professionnel, conçu pour intégrer plusieurs modules de **prédiction** et d’**analyse intelligente de données**.

---

## 🧠 Objectif du projet

Fournir une **plateforme interactive** permettant d'explorer 4 cas d'usage de l'intelligence artificielle appliquée à des données externes :

- 🌤️ Prévision météorologique
- 🌬️ Analyse de la qualité de l’air
- 👥 Prédiction de churn client
- 🛍️ Prévision des ventes

---

## 🗂️ Arborescence du projet

projet_stage_ete_2025/
│
├── app_streamlit/
│ ├── main.py # Dashboard principal
│ ├── air_quality_app.py # Interface Qualité de l'air
│ ├── weather_app.py # Interface Météo
│ ├── churn_app.py # Interface Churn client
│ ├── sales_app.py # Interface Prévision ventes
│
├── src/
│ ├── air_quality_connector.py # Récupération données qualité de l'air via OpenWeather
│ ├── weather_connector.py # Connexion météo via OpenWeather
│ ├── churn_model.py # Modèle XGBoost pour churn
│ ├── sales_model.py # Modèle RandomForest ou ARIMA pour ventes
│
├── notebooks/
│ ├── test_air_quality.ipynb # Test du connecteur air
│ ├── test_weather.ipynb # Test du connecteur météo
│ ├── modelisation_churn.ipynb # Analyse churn + XGBoost
│ ├── forecast_sales.ipynb # Analyse ventes + ARIMA
│
├── .env # Clés API
├── requirements.txt # Dépendances
└── README.md # Ce fichier

yaml
Copy
Edit

---

## ⚙️ Technologies utilisées

- 🐍 Python 3.11
- 📈 Streamlit
- 📊 Pandas, NumPy, Plotly, Seaborn, Matplotlib
- 🤖 XGBoost, RandomForest, ARIMA
- 🔗 OpenWeather API
- 💻 Jupyter Notebooks

---

## 📦 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/ton-utilisateur/projet_stage_ete_2025.git
cd projet_stage_ete_2025
2. Créer un environnement virtuel
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
3. Installer les dépendances
bash
Copy
Edit
pip install -r requirements.txt
4. Ajouter la clé OpenWeather
Crée un fichier .env à la racine et ajoute :

ini
Copy
Edit
OPENWEATHER_API_KEY=f0ea4e92f1e88b9b1574be33bbad517f
🚀 Lancer l'application
Depuis le dossier app_streamlit :

bash
Copy
Edit
streamlit run main.py
📌 Modules disponibles
🌤️ Météo
Récupération des prévisions sur 5 jours

Visualisation par courbe de température

Affichage par ville

🌬️ Qualité de l’air
Analyse des particules PM10, O3, NO2, etc.

Bar chart dynamique

Données par ville

👥 Churn client
Prédiction avec XGBoost entraîné sur le dataset Telco

Courbe ROC et matrice de confusion

Affichage des probabilités de churn

🛍️ Prévision des ventes
Modèle Random Forest ou ARIMA

Visualisation de la tendance

Simulation de scénario

✨ Auteur
👩‍💻 Yasmine Abdennadher
Ingénieure en Data Science & Intelligence Artificielle
Stage chez YottaByte – Été 2025

📞 Contact
Pour toute question ou suggestion :
📧 yasmine.abdennadher@example.com (à adapter)

✅ À venir
🔐 Authentification par utilisateur

💾 Sauvegarde des prédictions

🌍 Intégration de nouvelles APIs (trafic, finance…)



---

## 📦 Modules Fonctionnels

### 1. 🌫️ Qualité de l'air

- **API utilisée :** [OpenAQ](https://docs.openaq.org/)
- **Fonctionnalité :**
  - Visualisation des polluants d'une ville
  - Camembert, radar, bar chart interactifs
  - Détection de l’AQI avec échelle descriptive

### 2. 🌦️ Météo

- **API utilisée :** [OpenWeatherMap](https://openweathermap.org/)
- **Fonctionnalité :**
  - Température, humidité, pression, vent
  - Comparaison de plusieurs villes
  - Visualisation interactive avec Plotly

### 3. 👥 Churn Client

- **Données :** Telco Customer Churn (Kaggle)
- **Modèle :** XGBoost
- **Interface :**
  - Formulaire utilisateur
  - Affichage de la probabilité de churn

### 4. 📈 Prévision de Ventes

- **Données :** jeu synthétique / import via CSV
- **Modèle :** Prophet / SARIMAX
- **Interface :**
  - Upload de fichier CSV
  - Forecast dynamique

---

## ▶️ Lancement de l’application

Depuis le répertoire `app_streamlit` :

```bash
streamlit run main.py
