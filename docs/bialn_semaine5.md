📅 Mardi 6 août 2025
✅ Travaux réalisés

Finalisation et tests du module Air Quality :

Chargement optimisé des datasets (stations et mesures).

Ajout de visualisations interactives (évolution du PM2.5 et PM10 par ville).

Intégration dans l’interface Streamlit avec filtres de ville et période.

Débogage du module Météo :

Correction d’un bug sur le cache des appels API.

Meilleure gestion des valeurs manquantes.

Harmonisation des couleurs et styles sur tous les graphiques pour cohérence visuelle.

📅 Mercredi 7 août 2025
✅ Travaux réalisés

Réorganisation des scripts de prédiction pour tous les modèles :

Structure unifiée predict_X() (X = churn, ventes, météo, air, covid, nutrition, ecommerce).

Export systématique des modèles en .joblib.

Création d’un dossier central /models pour regrouper tous les modèles entraînés.

Documentation initiale des modèles (description des entrées, sorties et métriques de perf).

📅 Jeudi 8 août 2025
✅ Travaux réalisés

Mise en place de la base du Chatbot :

Scripts chat_api.py, retriever.py, qa_chain.py et index_docs.py.

Configuration d’un modèle local de question/réponse (DistilBERT).

Indexation initiale de la documentation technique et des fichiers de code.

Test de l’API Flask du chatbot avec requêtes simples.

Préparation d’un plan pour connecter le chatbot aux modèles prédictifs.

📅 Lundi 11 août 2025
✅ Travaux réalisés

Ajout des descriptions fonctionnelles de tous les modèles (churn, ventes, météo, air, covid, nutrition, ecommerce) dans docs/models_overview.md pour enrichir la base du chatbot.

Modification du pipeline d’indexation (index_docs.py) pour inclure automatiquement ces nouvelles descriptions.

Première réflexion sur la détection d’intention dans le chatbot pour distinguer une question classique d’une demande de prédiction.

📅 Mardi 12 août 2025
✅ Travaux réalisés

Développement de la fonction handle_prediction_request() dans chat_api.py :

Routage automatique des requêtes vers le modèle correspondant si l’intention est une prédiction.

Gestion des cas simples (ex : "Prédit les ventes pour demain").

Tests unitaires sur la connexion Chatbot ↔ Modèles réels.

Début de la préparation du docker-compose pour intégrer le service chatbot à la plateforme globale.