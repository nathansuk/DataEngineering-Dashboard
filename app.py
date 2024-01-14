from flask import Flask
from flask import render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongo")


@app.route("/")
def hello_world():
    return render_template('index.html')
