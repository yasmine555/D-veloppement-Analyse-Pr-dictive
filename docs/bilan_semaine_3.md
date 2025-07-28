✅ Bilan de la journée – Lundi 14 juillet 2025
Travaux réalisés :

Finalisation des visualisations avancées :
• Churn selon tenure, contrat, type d’accès Internet, etc.
• Graphiques interactifs avec Plotly
• Heatmaps avec Seaborn
• Barplots avec Matplotlib
• Mise en page claire et professionnelle du notebook

Nettoyage et finalisation complète du notebook de visualisation

Ajout du connecteur COVID-19 (Our World In Data) :
• Téléchargement automatisé des données mondiales
• Filtrage par pays et période
• Normalisation des colonnes
• Génération de courbes (cas, décès, vaccination)
• Visualisations comparatives multi-pays avec Seaborn et Plotly


Bilan du mardi 15 juillet 2025
Travail réalisé :
Développement du deuxième connecteur avancé :

Création du connecteur openfoodfacts_connector.py permettant d’interroger l’API OpenFoodFacts.

Fonctionnalités : recherche produit par nom ou code-barres, extraction des informations nutritionnelles, catégories, pays, image.

Résultat structuré sous forme de DataFrame pour faciliter l’intégration dans les modèles et interfaces.

Ce connecteur apporte une source externe qualitative pour enrichir les données métiers et peut servir à des analyses liées aux produits.

Préparation de la prévision de ventes (phase initiale) :

Mise en place de la structure de base pour le futur modèle de prévision.

Choix d’une source réelle de données (API DummyJSON) pour simuler un historique de ventes e-commerce.

Conception du pipeline de récupération des données depuis l’API, simulation d’une série temporelle par date fictive.

Organisation des livrables et planification :

Création des dossiers et fichiers nécessaires : notebooks, scripts, API, interface Streamlit.

Planification claire pour avancer sur la modélisation, l’intégration et le rapport.

Résultats obtenus :
Un connecteur externe robuste et testé, prêt à être utilisé dans des analyses plus larges.

Un pipeline d’extraction de données de ventes démarré avec succès.

Une base solide pour la construction du modèle de prévision, prête pour entraînement.

Difficultés rencontrées :
Ajustement du format des données API pour répondre aux besoins du modèle.

Synchronisation entre les sources de données et la structure des scripts.

📅 Bilan du mercredi 16 juillet 2025
Travail réalisé :
Modélisation prédictive de la prévision de ventes :

Implémentation d’un modèle supervisé de régression (LinearRegression) pour prédire le total des ventes à partir d’une variable temporelle.

Construction des features temporelles simples (t comme indice croissant).

Entraînement du modèle sur les données simulées extraites de l’API.

Évaluation initiale des performances via RMSE, avec sauvegarde du modèle.

Mise en place des bases pour intégration dans Streamlit et API Flask :

Préparation d’un notebook d’exploration (forecast_model.ipynb) pour la visualisation et le test manuel des résultats.

Conception de la structure des fichiers pour future intégration de l’API /predict-sales.

Définition des futures étapes pour la mise en place d’une interface utilisateur interactive.

Documentation et planification des prochaines étapes :

Préparation d’un bilan structuré pour communiquer clairement l’avancement.

Planification du focus des prochains jours sur l’intégration API et interface, avec tests utilisateurs.

Résultats obtenus :
Modèle de prévision opérationnel, capable de prédire les ventes avec une erreur maîtrisée.

Structuration claire et modulaire du projet pour faciliter l’évolution et la maintenance.

Base prête pour la mise en production en API et interface utilisateur.



📝 Bilan du jeudi 17 juillet 2025
✅ 1. Interface Streamlit de prévision de ventes
Création de streamlit_app/sales_forecasting.py :

Chargement et mise en cache du modèle

Sélection intuitive d’une date future

Calcul de la variable temporelle t

Affichage professionnel de la prédiction ou message d’erreur en cas de date passée

📌 Résultat visuel : prédiction claire en unités de vente, design épuré et ergonomique.

✅ 2. Déploiement de l’API Flask dédiée
Développement de forecast_api/predict.py :

Endpoint /predict_sales en GET

Validation stricte du paramètre date

Rejet des formats invalides ou antériorité

Réponse JSON structurée contenant la date et la valeur prédite

🛠️ Assez robuste pour une intégration future dans du front-end ou un produit métier.

✅ 3. Découpage fonctionnel & architecture claire
Séparation des responsabilités :

sales_forecasting.py : entraînement du modèle

sales_model.pkl : modèle entraîné dans models/

streamlit_app/ : interface reactive

forecast_api/ : API pluggable et extensible

🧩 Résultat : code modulaire, isolable, facile à maintenir.

✅ 4. Qualité et maintenabilité
Utilisation de @st.cache_resource pour l’efficacité avec Streamlit

Vérification complète des erreurs dans l’API

Documentation succincte dans chaque module

Préparation directe pour amélioration modèle (Prophet, LSTM…)


📅 Bilan du Vendredi 18 Juillet 2025 – Semaine 3
Finaliser les fonctionnalités interactives du dashboard IA.

Réorganiser l’interface pour rendre les modules Churn et Forecast plus modernes et attractifs.

Ajouter les zones de saisie utilisateur et les prédictions en temps réel pour les deux modèles.

Commencer la refonte esthétique pour donner une image professionnelle et impressionnante du projet.

Préparer l’ajout des pourcentages de confiance des prédictions (feature avancée prévue pour fin de journée).