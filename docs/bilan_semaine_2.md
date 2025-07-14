📅lundi 7 juillet 2025
✅ Travaux réalisés :
Organisation de tous les notebooks et scripts dans une structure modulaire pour un usage futur.
Comparaison finale des performances des 3 modèles (Logistic Regression, Random Forest, XGBoost) :
Courbes ROC superposées avec RocCurveDisplay pour visualiser la performance relative.
Choix confirmé de XGBoost comme meilleur modèle (précision, f1-score et AUC).
Refactorisation du code d’évaluation pour rendre l’évaluation reproductible.
Création du fichier model_telco.py centralisant :
Le chargement/nettoyage du dataset
L’entraînement du modèle

📅mardi 8 juillet 2025
✅ Travaux réalisés :
 Sauvegarde du modèle XGBoost dans models/model_churn_xgb.pkl
 Création d’un script de test pour prédire à partir d’un CSV
 Mise en place d’un module propre predict_churn.py avec une fonction réutilisable predict_from_df()
 Test réussi de prédictions sur de nouvelles données

📅 Mercredi 9 juillet 2025
✅ Travaux réalisés :

Intégration du modèle XGBoost dans une application Streamlit interactive
Gestion des cas particuliers (valeurs manquantes dans TotalCharges)
Amélioration de la fonction predict_from_df() pour maintenir la cohérence des prédictions
Affichage des prédictions avec possibilité de téléchargement CSV
Test complet et fonctionnement stable de l’interface utilisateur

🧾 Bilan du Jeudi 10 juillet 2025
✅ Travaux réalisés :

Création et test d'une API Flask fonctionnelle :
Route /predict pour fichier CSV
Route /predict/json pour appels JSON
Prétraitement automatique dans l’API
Testé avec httpie et script Python ✅
Développement d’une interface utilisateur Streamlit :
Chargement de fichiers clients
Affichage des prédictions en temps réel
Ajout d’un graphique interactif via Plotly
Option de téléchargement des résultats
Affichage clair des résultats et messages

📅 Vendredi 11 juillet 2025
✅ Travaux réalisés :
Création du notebook visualisation_telco.ipynb dédié à l’analyse exploratoire des données clients.
Exploration visuelle du dataset avec plusieurs bibliothèques de visualisation :
Seaborn : heatmap, boxplots, histogrammes
Matplotlib : répartition simple du churn
Plotly : graphiques interactifs (pie, bar, sunburst)
Analyse ciblée du churn selon plusieurs variables clés :
Type de contrat
Ancienneté (tenure)
Charges mensuelles et totales
Type d’accès Internet