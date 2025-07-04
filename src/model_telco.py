import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)

    # Nettoyage de base
    df = df[df["TotalCharges"] != " "]
    df["TotalCharges"] = df["TotalCharges"].astype(float)

    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Colonnes inutiles
    df.drop(["customerID"], axis=1, inplace=True)

    # Encodage des variables catégorielles
    df = pd.get_dummies(df, drop_first=True)

    return df

def train_logistic_model(df):
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "model": model,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "y_proba": y_proba
    }

def evaluate_model(results):
    print("Classification Report:\n", classification_report(results["y_test"], results["y_pred"]))
    print("Confusion Matrix:\n", confusion_matrix(results["y_test"], results["y_pred"]))
    print("ROC AUC:", roc_auc_score(results["y_test"], results["y_proba"]))
