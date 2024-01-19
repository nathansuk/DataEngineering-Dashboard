from flask import Flask
from flask import render_template
import pymongo
import pandas as pd
import plotly.express as px

app = Flask(__name__, static_url_path='/static')
client = pymongo.MongoClient("mongo")

#Connexion et import jeu de données
client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
db_series = client["admin"]
collection_games = db_series['instantGaming']
cursor = collection_games.find()
documents_list = list(cursor)
data = pd.DataFrame(documents_list)
data = data.drop(columns=["_id"])

#Graph prix moyen par année d'un jeu
data_date = data[~data["tags"].astype(str).str.contains("DLC", na=False)]
data_date = data_date.dropna(subset=["date_published"]).reset_index(drop=True)
data_date["date_published"] = data_date["date_published"].str.replace('-PC', '')
data_date.loc[:, "date_published"] = data_date["date_published"].str[-4:]
data_date = data_date[data_date["date_published"].astype(str).str.match(r'\d{4}$')]
new_dataframe = pd.concat([data_date["date_published"], data_date["final_price"]], axis=1)
average_prices_by_year = new_dataframe.groupby("date_published")["final_price"].mean().reset_index()

#Graph autre

fig_date = px.line(average_prices_by_year, x='date_published', y='final_price', title='Prix moyen par année d\'un jeu (année de référence: 2024)',
              labels={'date_published': 'Année de publication', 'final_price': 'Prix du moyen d\'un jeu'},
              markers=True, line_shape='linear')

@app.route("/")
def hello_world():
    return render_template('index.html', plot=fig_date.to_html(), tables=[data_date.to_html(classes='data')])

if __name__ == '__main__':
    app.run(debug=True)
