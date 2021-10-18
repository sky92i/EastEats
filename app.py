import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json

app = Flask(__name__)

""" port = os.environ.get("MONGO_SERVER_PORT",9990)
host = os.environ.get("MONGO_SERVER_HOST",9990)
username = os.environ.get("MONGO_USERNAME",9990)
password = os.environ.get("MONGO_PASSWORD",9990) """

#client = MongoClient(username=username, port=int(port), host=host, password=password)
client = MongoClient(username='comp3122', port=27017, host='mongo', password='12345')

@app.route('/')
def home():
    return f"Hello world!"

#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)