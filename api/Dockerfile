# Base légère pour rester <150MB
FROM python:3.12-alpine

# Set workdir
WORKDIR /app

# Installer dépendances (FastAPI + Redis client)
RUN pip install --no-cache-dir fastapi uvicorn redis

# Copier le code
COPY . .

# Expose le port
EXPOSE 8080

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
