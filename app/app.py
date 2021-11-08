import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

try:
    # connect mongodb with the environment variables
    client = MongoClient(f'mongodb://{os.environ.get("MONGO_USERNAME")}:{os.environ.get("MONGO_PASSWORD")}@{os.environ.get("MONGO_SERVER_HOST")}:27017/{os.environ.get("MONGO_DATABASE")}?authSource=admin')
    client.server_info() # check database connection
    print ("[v] Database connection success")
except Exception as e: # print error and exit
    print ("[x] Database connection error")
    if e.code == 18: print ("[x] Database authentication failed.")
    print ("Error details: ", e.details)

db = client["EasyEats"]

def remove_id(data):
    data.pop('_id')
    return data

@app.route('/')
def home():
    return f"Hello world!"

@app.route('/order/<order_id>', methods=['GET'])
def get_order_details(order_id):
    data = [remove_id(i) for i in db.order.find({"order_id":order_id})]
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error":"not found"}), 404

@app.route('/orders/<order_id>/accept_pos_order', methods={'POST'})
def accept_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        if request:
            request_body = request.json
            if not request_body["reason"]:
                return jsonify({"error":"reason must be given"}), 400
        else:
            return jsonify({"error":"reason must be given"}), 400

        if data[0]['current_state'] == 'accepted':
            return jsonify({"error":"order is already accepted"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'accepted'}})
            return jsonify({}), 204

@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])
def deny_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        allowed_codes = ["store_closed","pos_not_ready","pos_offline","item_availability","missing_item","missing_info","pricing","capacity","address","special_instructions","other"]
        if request:
            request_body = request.json
            if not request_body["reason"]:
                return jsonify({"error":"reason must be given"}), 400
            elif not (request_body["reason"]["explanation"] and request_body["reason"]["code"]):
                return jsonify({"error":"reason is not complete"}), 400
            elif request_body["reason"]["code"] not in allowed_codes:
                return jsonify({"error":"reason code invalid"}), 400
        else:
            return jsonify({"error":"reason must be given"}), 400

        if data[0]['current_state'] == 'denied':
            return jsonify({"error":"order is already denied"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'denied'}})
            return jsonify({}), 204

@app.route('/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        
        allowed_codes = ["out_of_items","kitchen_closed","customer_called_to_cancel","restaurant_too_busy","cannot_complete_customer_note","other"]
        allowed_parties = ["merchant", "customer"]

        if request:
            request_body = request.json
            if not request_body["reason"]:
                return jsonify({"error":"reason must be given"}), 400
            elif not request_body["cancelling_party"]:
                return jsonify({"error":"cancelling party must be given"}), 400
            elif request_body["reason"] not in allowed_codes:
                return jsonify({"error":"reason code invalid"}), 400
            elif request_body["cancelling_party"] not in allowed_parties:
                return jsonify({"error":"invalid cancelling party"}), 400
        else:
            return jsonify({"error":"reason must be given"}), 400

        if data[0]['current_state'] == 'canceled':
            return jsonify({"error":"order is already canceled"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'canceled'}})
            return jsonify({}), 200

@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])
def update_delivery_status(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        request_body = request.json
        allowed_status = ["status","arriving","delivered"]
        if request_body["status"] not in allowed_status:
            return jsonify({"error":"Delivery status is not allowed"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'status':request_body["status"]}})
            return jsonify({}), 204

#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)