from flask import request, jsonify
import pymongo.errors as errors
from product import products
from app import db
from bson.objectid import ObjectId

products_c = db["products"]


@products.route('/', methods=["GET"])
def get_all_products():
	products = list(products_c.find({}))
	final_products = [ ]
	for product in products:
		product["_id"] = str(product["_id"])
		final_products.append(product)

	return jsonify(final_products)

@products.route('/', methods=["POST"])
def create_product():
	body = request.json
	product = products_c.insert_one(body)
	return jsonify({
		"id": str(product.inserted_id),
		"msg": "Success"
	}), 201

@products.route('/<id>', methods=["PUT"])
def update_product(id: int):
	update_payload = request.json
	products_c.update_one({ "_id": ObjectId(id) }, {
		"$set": update_payload
	})
	return jsonify({
		"msg": "Success"
	})

@products.route('/<id>', methods=["DELETE"])
def delete_product(id: int):
	products_c.delete_one({ "_id": ObjectId(id) })
	return jsonify({
		"msg": "Success"
	})