
# Projet Data Enginnering

Ce projet consiste en un dashboard présentant des données "scrapées" depuis le site https://steampowered.com

Le projet est constitué de 4 sous-parties : 

- Le dashboard développé avec Python et le framework Flask
- Un scrapper avec la librairie scrapy
- Une base de données MongoDB
- Une interface MongoExpress permettant d'adminsitrer la base de données Mongo.

Ces 4 sous-projets sont réunis et peuvent être démarrés simultanément grâce à un docker compose.

## Installation 

Clonez le dépôt : 

```
git clone https://github.com/nathansuk/DataEngineering-Dashboard.git
```

- Démarrez une instance de Docker Desktop.
- Rendez-vous dans le répertoire du projet cloné puis exécutez la commande : 

```
docker compose up
```

- Les différentes images vont être installées puis les conteneurs seront démarrés.

## Accès aux services

Les services sont accessibles via les liens suivants : 

- **Dashboard :** http://localhost:8000
- **Host Mongodb :** http://localhost:27017
- **MongoExpress :** http://localhost:8081


