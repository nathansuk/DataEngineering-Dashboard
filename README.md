
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

### Accès aux services

Les services sont accessibles via les liens suivants : 

- **Dashboard :** http://localhost:8000
- **Host Mongodb :** http://localhost:27017
- **MongoExpress :** http://localhost:8081



 ## Documentation technique ##

## 1) Le scraping

Pour obtenir les données, un script de scraping a été créé à l’aide de la librairie Scrapy.
La collecte des données s’effectue sur la page :

https://www.instant-gaming.com/fr/rechercher/

Le module de recherche d'Instants Gaming possède une pagination avec + de 250 pages de 60 (max) jeux par page.
Il faut donc dans un premier temps récupérer le nombre de pages grâce à l'élément HTML suivant.

![Alt text](https://i.ibb.co/7vq3bNZ/Capture-d-cran-2024-01-30-144054.png)

Puis de parser chaque liens de chaque jeu

![Alt text](https://i.ibb.co/PNV7yLh/Capture-d-cran-2024-01-30-151225.png)

Il s’agira ensuite de récupérer les informations pertinentes sur chaque page de chaque jeu  à savoir : 

```python
class UrlStock(scrapy.Item):
    title = scrapy.Field()
    developers = scrapy.Field()
    publisher = scrapy.Field()
    ig_review_average = scrapy.Field()
    ig_review_number = scrapy.Field()
    discounted = scrapy.Field()
    date_published = scrapy.Field()
    final_price = scrapy.Field()
    tags = scrapy.Field()
    genres = scrapy.Field()
    original_selling_platform = scrapy.Field()
    playable_platform = scrapy.Field()
    editions = scrapy.Field()
```

### Données

- **titre** : titre du jeu
- **developers** : le.s développeur.s
- **publisher** : l’éditeur
- **ig_review_average**: la note moyenne (donnée par les utilisateurs)
- **ig_review_number** : nombre de notation
- **discounted**: Montant de la réduction (valeur absolue, en %)
- **date_published**: date de publication
- **final_price**: prix à l’achat après réduction sur instant gaming
- **tags**: sous catégories du jeu
- **genres**: genre.s de jeu
- **original_selling_platform**: plateforme où le jeu est en vente à l’origine (EA Store,  Steam, Microsoft etc..)
- **playable_platform**: Plateformes sur lesquelles le jeu est jouable (MacOS, Windows, Linux)
- **editions**: Liste des éditions du jeu si il en existe (Standard, Premium, Complete etc..)

Ces données sont récupérées depuis les composants HTML suivants : 

```python
title = str(item.css('.game-title::text').extract_first())
developers = item.xpath('//a[@content="Developers"]/text()').get() 
publisher = item.xpath('//a[@content="Publishers"]/text()').get()
ig_review_average = str(item.css(".show-more-reviews").css(".high").css("div::text").extract_first())  
ig_review_number = str(item.css('div.based span.link::text').extract_first())
discounted = str(item.css('.discounted::text').extract_first())
date_published = str(item.css('.release-date::text').extract_first())
final_price = str(item.css('.total::text').extract_first()) 
tags = str(item.css('a.searchtag::text').getall())
genres = str(item.css('div.genres a.tag::text').getall())
original_selling_platform = str(item.css('div.subinfos a.platform').get())
playable_platform = item.css('select#platforms-choices option::attr(value)').getall() or ['PC']
editions = { str(option.css('::text').get().strip().replace('\u20ac', '')): str(option.css('::attr(data-product-price)').get()).replace('\u20ac', '') for option in item.css('select#editions-choices option') }
```

Les données sont ensuite enregistrées dans le fichier : __{root}/scraping/instantGaming.json__

## Execution du scraping

Pour executer le script du scraping : 
```shell
cd scraping
scrapy crawl instantGaming -o instantGaming.json
```

# Docker & docker compose

Nous avons fait le choix de créer 3 conteneurs différents pour 3 services à savoir : 
- L’application Flask (python)
- La base de données mongodb
- mongo-express, client web basé sur le framework express permettant d’administrer la base de données.

## Application web
Les instructions sont renseignées dans le fichier ./Dockerfile

```
syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /code
ENV FLASK_APP=app.py
ENV LISTEN_PORT=5000
EXPOSE 5000
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]
```

1) L’image se base sur la version “slim” de python 3.7, l’image alpine causait des problèmes au niveau de l’installation des dépendances (c.f :https://stackoverflow.com/questions/60086741/docker-so-slow-while-installing-pip-requirements) 
2) Le code sera placé dans le répertoire /code
3) (Variable d’environnement FLASK_APP) Le fichier de démarrage par défaut du dashboard de l’application est app.py
4) (Variable d’environnement LISTEN_PORT) Le port mappé par défaut sera 5000
5) Copie du fichier requirements.txt dans le conteneur
6) Installation des dépendances renseignées dans requirements.txt
7) Démarrage du service (flask run ⇔ python3 app.py)


Nous avons ensuite fait le choix d’utiliser docker-compose afin de mieux orchestrer le démarrage et les dépendances entre les services, créer des volumes persistants et un network bridge entre les services.

Les instructions se trouvent dans le fichier : **compose.yaml**

### Instructions du conteneur “mongo”
```
version: '3.1'
services:
  mongo:
    image: mongo:latest
    hostname: mongo_database
    ports:
      - "27017:27017"
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
```

1) L’image :latest de mongo est utilisée
2) Le nom d’hôte (pour y accéder depuis un autre container sur le même network) sera __mongo_database__
3) Le port associé : **27017**
4) Le conteneur est redémarré en cas d’arrêt 
5) Définitions des variables d’environnement (user: root, password: example)

### Instructions dashboard, conteneur “web”
```
  web:
    build: .
    ports:
      - "5000:5000"
    links:
      - mongo
``` 

1) Le build se fait grâce au Dockerfile présent à la racine
2) Port: 5000
3) Lien avec le service **“mongo”**, le démarrage du conteneur se fait une fois que “mongo” est démarré

### Instructions mongo-express: 
```
  mongo-express:
    image: mongo-express
    depends_on:
      mongo:
        condition: service_started
    restart: always
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example
      ME_CONFIG_MONGODB_URL: mongodb://root:example@mongo:27017/
      ME_CONFIG_BASICAUTH_USERNAME: web
      ME_CONFIG_BASICAUTH_PASSWORD: web
      ME_CONFIG_MONGODB_ENABLE_ADMIN: 'true'
      ME_CONFIG_MONGODB_PORT: 27017
      ME_CONFIG_MONGODB_SERVER: 'mongo'
```

1) L’image mongo-express:latest est utilisée
2) Le service dépend également du conteneur “mongo”
3) On spécifie que le service doit être complètement démarré pour lancer le conteneur (pas de healthcheck)
4) Redémarrage si nécessaire
5) Ports associés 8081 (accessible à l’URL : http://localhost:8081)
6) Définitions des variables d’environnement (connexion à la base de données, authentification sur l’administration web, autorisation du compte administrateur, port et hôte de la base de données)

#### Grâce à docker-compose, il est possible de (re) démarrer tous les services en même temps grâce à la commande **docker compose up**.


### Accès aux services

- Dashboard : http://localhost:8000
- Host Mongodb : http://localhost:27017
- MongoExpress : http://localhost:8081

# MongoDB

A partir de ce jeu de données au format JSON, il est possible de remplir la base de données MongoDB. Ce choix de moteur est motivé par le fait que chaque entrées (documents) possède une structure similaire qui diffère parfois (liste des editions par exemple) et ne nécessite pas de relations particulières (dans le contexte de l’exercice).

L’ajout des données depuis le fichier .json se fait à partir de la méthode : populate_database() de l’objet DatabaseClient (database_client.py)










