FROM python:3.11-slim

# Installer git et dépendances utiles
RUN apt-get update && apt-get install -y git build-essential

# Créer le dossier de travail
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le reste du projet
COPY . .

# Lancer ton app
CMD ["python", "app.py"]
