# Bilan - Semaine 1 - Yasmine Abdennadher

##  Jour 1 – Lundi 1er juillet 2025

## Travaux réalisés :
- Compréhension complète du sujet de stage : développement d’une plateforme d’analyse prédictive basée sur la collecte de données externes et la modélisation ML.
- Mise en place de l’arborescence du projet (`src/`, `data/`, `docs/`, `notebooks/`…).
- Création du fichier `.env` pour sécuriser les clés d’API.
- Élaboration et test d’un **connecteur API météo** via OpenWeatherMap.
- Installation des bibliothèques Python nécessaires (`requests`, `python-dotenv`).
- Affichage des 5 prochaines prévisions météo via un script Python structuré et commenté.

### 🔧 Fichiers créés :
- `src/weather_connector.py` : script de récupération météo
- `.env` : clé API
- `requirements.txt` : bibliothèques
- Structure de projet complète

### 📌 Remarques :
- L’utilisation de la librairie `dotenv` permet de garder la clé API confidentielle.
- Le connecteur est fonctionnel et retourne des données structurées.
- Prête à ajouter d'autres connecteurs et commencer la normalisation.

---

## 📅 Jour 2 – Mardi 2 juillet 2025

### ✅ Travaux réalisés :
- Sélection et téléchargement du dataset **Telco Customer Churn** depuis Kaggle.
- Intégration du fichier CSV dans le dossier `data/` du projet.
- Développement d’un connecteur de type "fichier local" :
  - Script `telco_loader.py` permettant de charger et nettoyer les données clients.
  - Conversion des colonnes booléennes (Yes/No → 1/0), nettoyage de `TotalCharges`, retrait des lignes vides.
- Création d’un notebook `exploration_telco.ipynb` pour visualiser et explorer les données :
  - Répartition du churn
  - Corrélations numériques
  - Influence du contrat et de l'ancienneté (`tenure`) sur le churn
- Correction de l'import dynamique dans le notebook pour que le module `src` soit reconnu (`sys.path.append(...)`).
- Documentation de cette source de données dans le fichier `docs/veille_sources_donnees.md`.

### 🔧 Fichiers créés :
- `src/telco_loader.py` : connecteur pour le CSV Telco
- `notebooks/exploration_telco.ipynb` : visualisation des données
- `data/WA_Fn-UseC_-Telco-Customer-Churn.csv` : jeu de données brut
- Mise à jour du `README.md` et du fichier de veille

### 📌 Remarques :
- Le dataset est très adapté à un cas de churn client, avec des variables claires.
- Les premières visualisations montrent une influence de certains facteurs (contrat, tenure, etc.).
- Le connecteur est propre, modulaire et prêt à être utilisé pour l'entraînement de modèles.


## 📅 Jour 3 – Mercredi 3 juillet 2025

### ✅ Travaux réalisés :
- Nettoyage et préparation du dataset Telco (encodage, suppression colonnes inutiles)
- Implémentation d’un modèle de régression logistique pour prédire le churn
- Évaluation via classification report, matrice de confusion, ROC AUC
- Visualisation de la courbe ROC
- Organisation claire en deux fichiers : script Python + notebook de modélisation
