from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
mongo_client = MongoClient("mongodb://localhost:27017/restaurant")
db = mongo_client["restaurant"]

from product import products
from users import users
from orders import orders


app.register_blueprint(products, url_prefix='/api/products')
app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(orders, url_prefix='/api/orders')


if __name__=="__main__":
	app.run(host="localhost", port=8000, debug=True)