import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json

app = Flask(__name__)

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
    #TODO
    return 204

@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])
def deny_order(order_id):
    #TODO
    return 204

@app.route('/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    #TODO
    return 200

@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])
def update_delivery_status(order_id):
    #TODO
    return 204

#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)