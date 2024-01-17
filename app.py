from flask import Flask
from flask import render_template
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

app = Flask(__name__)
client = MongoClient("mongo")

df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 20, 15, 25]
})

fig = px.bar(df, x="Category", y="Value", title="Exemple de graphique Plotly")


@app.route("/")
def hello_world():
    return render_template('index.html', plot=fig.to_html())


if __name__ == '__main__':
    app.run(debug=True)
