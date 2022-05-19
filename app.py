from flask import Flask
from pymongo import MongoClient
from product import products

app = Flask(__name__)
mongo_client = MongoClient("mongodb://localhost:27017/restaurant")
db = mongo_client["restaurant"]

app.register_blueprint(products, url_prefix='/api/products')


if __name__=="__main__":
	app.run(host="localhost", port=8000, debug=True)