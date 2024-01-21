import pandas as pd
import pymongo
from datetime import datetime

def populate_db():

    data = pd.read_json("../scraping/instantGaming.json")

    data = data[data["url"].isna()].reset_index(drop=True)
    data = data.drop(columns=["url"])

    print(data.dtypes)

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

    print()

    print(data.dtypes)

    data_dict = data.to_dict(orient='records')

    client = pymongo.MongoClient("127.0.0.1")

    print(client.list_database_names())

    db_series = client["admin"]

    print(db_series)

    collection_games = db_series['instantGaming']

    #collection_games.insert_many(data_dict)

    print(collection_games.count_documents({}))

populate_db()

