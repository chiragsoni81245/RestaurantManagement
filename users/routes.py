from flask import request, jsonify
from users import users
from app import db
from bson.objectid import ObjectId

users_c = db["users"]
orders_c = db["orders"]


@users.route('/', methods=["GET"])
def get_all_users():
	users = list(users_c.find({}))
	final_users = [ ]
	for user in users:
		user["_id"] = str(user["_id"])
		final_users.append(user)

	return jsonify(final_users)

@users.route('/', methods=["POST"])
def create_user():
	body = request.json
	user = users_c.insert_one(body)
	return jsonify({
		"id": str(user.inserted_id),
		"msg": "Success"
	}), 201

@users.route('/<id>', methods=["PUT"])
def update_user(id):
	update_payload = request.json
	users_c.update_one({ "_id": ObjectId(id) }, {
		"$set": update_payload
	})
	return jsonify({
		"msg": "Success"
	})

@users.route('/<id>', methods=["DELETE"])
def delete_product(id):
	users_c.delete_one({ "_id": ObjectId(id) })
	return jsonify({
		"msg": "Success"
	})

@users.route('/<id>/orders', methods=["GET"])
def get_my_orders(id):
	orders = list(orders_c.find({ "userId": id }, {'_id': 1, 'products': 1}))
	final_orders = [ ]
	for order in orders:
		order["_id"] = str(order["_id"])
		final_orders.append(order)

	return jsonify(final_orders)