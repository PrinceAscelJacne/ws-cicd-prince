FROM python:3.12-slim

# TODO 1 : ajouter le label org.opencontainers.image.source qui relie l'image à votre dépôt GitHub
#          (valeur : https://github.com/<utilisateur>/ws-cicd-<prenom>)
LABEL org.opencontainers.image.source="https://github.com/princeasceljacne/ws-cicd-prince"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# TODO 2 : déclarer l'argument APP_VERSION (valeur par défaut : dev)
#          et l'exposer dans une variable d'environnement du même nom
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

# TODO 3 : créer un utilisateur non-root et l'utiliser pour lancer l'application
RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
