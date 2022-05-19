from flask import request, jsonify
from orders import orders
from app import db
from bson.objectid import ObjectId

orders_c = db["orders"]
products_c = db["products"]


@orders.route('/', methods=["GET"])
def get_all_orders():
	orders = list(orders_c.find({}))
	final_orders = [ ]
	for order in orders:
		order["_id"] = str(order["_id"])
		final_orders.append(order)

	return jsonify(final_orders)

@orders.route('/', methods=["POST"])
def create_orders():
	body = request.json

	if("userId" in body and not body["userId"]):
		return jsonify({"error_msg": "Invalid User Id"}), 400
	
	if("products" in body ):
		if(type(body["products"])==list):
			if(len(body["products"])==0):
				return jsonify({"error_msg": "Order should have at least one product"}), 400
		else:
			return jsonify({"error_msg": "Invalid Data"}), 400
	else:
		return jsonify({"error_msg": "Invalid Data"}), 400

	for product_data in body["products"]:
		if( "id" not in product_data and "quantity" not in product_data ):
			return jsonify({"error_msg": "Invalid Data"}), 400
	
		product = products_c.find_one({ "_id": ObjectId(product_data["id"]) })
		if(not product):
			return jsonify({"error_msg": "Invalid Product ID {}".format(product_data["id"])}), 400
		if(product_data["quantity"]>product["quantity"]):
			return jsonify({"error_msg": "Product with id {} does not have quantity {}".format(product_data["id"], product_data["quantity"])}), 400

		# Lock the Quantity for that product of this order
		products_c.update_one({
			"_id": ObjectId(product_data["id"])
		}, {"$set": { "quantity": product["quantity"]-product_data["quantity"]  }})

	try:
		order = orders_c.insert_one(body)
	except:
		for product_data in body["products"]:
			product = products_c.find_one({ "_id": ObjectId(product_data["id"]) })
			products_c.update_one({
				"_id": ObjectId(product_data["id"])
			}, {"$set": { "quantity": product["quantity"]+product_data["quantity"]  }})	
			return jsonify({
				"error_msg": "Something went wrong"
			}), 500

	return jsonify({
		"id": str(order.inserted_id),
		"msg": "Success"
	}), 201