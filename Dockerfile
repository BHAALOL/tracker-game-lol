# Utilise une image Python légère
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY script_csv_dmg.py script_csv_dmg.py
COPY players.csv players.csv
#COPY .env .env
#COPY .env .env
# Installe les dépendances
RUN pip install -r requirements.txt

# Expose le port si nécessaire (utile pour les applications web, mais pas nécessaire ici)
# EXPOSE 8000

# Exposer les variables d'environnement
ENV CSV_FILE_PATH=${CSV_FILE_PATH}
ENV API_KEY=${API_KEY}

# Lance le script principal
CMD ["python", "script_csv_dmg.py"]

