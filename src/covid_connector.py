import requests
import pandas as pd

def get_covid_data(country="Tunisia", days=30):
    """
    Récupère les données de cas COVID des 30 derniers jours pour un pays.
    Source : https://disease.sh
    """
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays={days}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "timeline" not in data:
            raise ValueError(f"Pas de données pour le pays : {country}")

        cases = data["timeline"]["cases"]
        deaths = data["timeline"]["deaths"]
        recovered = data["timeline"].get("recovered", {})

        df = pd.DataFrame({
            "date": list(cases.keys()),
            "cases": list(cases.values()),
            "deaths": list(deaths.values()),
            "recovered": list(recovered.values()) if recovered else [None]*len(cases)
        })

        df["date"] = pd.to_datetime(df["date"])
        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    except requests.exceptions.RequestException as e:
        print("❌ Erreur API :", str(e))
        return pd.DataFrame()
    except Exception as e:
        print("❌ Erreur de traitement :", str(e))
        return pd.DataFrame()
