import pandas as pd
from pymongo import MongoClient


class DatabaseClient:

    #URI : "mongodb://root:example@mongo_database:27017"
    def __init__(self):
        self.client = MongoClient("127.0.0.1")

        if self.is_database_empty():
            print("La base de données est vide")
            self.populate_database()
            print("La base de données a été remplie")

        else:
            print("La base de données est déjà remplie.")

    def get_client(self):
        return self.client

    def get_instantgaming_series(self):
        return self.client["admin"]["instantGaming"]

    def get_data_as_dataframe(self):
        curseur = self.get_instantgaming_series().find()
        liste = list(curseur)
        return pd.DataFrame(liste).drop(columns="_id")

    def get_nb_document(self):
        return self.get_instantgaming_series().count_documents({})

    def is_database_empty(self):
        return self.get_nb_document() == 0

    def populate_database(self):
        data = pd.read_json("./scraping/instantGaming.json")
        data = data[data["url"].isna()].reset_index(drop=True)
        data = data.drop(columns=["url"])

        data["title"] = data["title"].astype(str)
        data["developers"] = data["developers"].astype(str)
        data["publisher"] = data["publisher"].astype(str)
        data["ig_review_average"] = data["ig_review_average"].replace('None', '-1').astype(float)
        data["ig_review_number"] = data["ig_review_number"].replace('None', '-1').astype(float)
        data["discounted"] = data["discounted"].replace('None', '0').astype(int)
        data["date_published"] = data["date_published"].astype(str)
        data["final_price"] = data["final_price"].replace('None', '0').astype(float)
        data["tags"] = data["tags"].replace('', 'None').astype(str)
        data["genres"] = data["genres"].astype(str)
        data["original_selling_platform"] = data["original_selling_platform"].astype(str)
        data["playable_platform"] = data["playable_platform"].astype(str)
        data["editions"] = data["editions"].replace('', 'None').astype(str)

        data_dict = data.to_dict(orient='records')

        self.get_instantgaming_series().insert_many(data_dict)