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

@app.route('/')
def home():
    return f"Hello world!"

#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)