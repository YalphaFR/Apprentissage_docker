#!/bin/bash

# Lancer la base de données
docker run -d --name db --network my-tiny-network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=workshop \
  -e PGDATA=/data \
  -v db-vol:/data \
  db


# Lancer l'application
docker run -d --name app --network my-tiny-network -p 8080:8080 app