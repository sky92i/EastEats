import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json

app = Flask(__name__)

port = os.environ.get("MONGO_SERVER_PORT",9990)
host = os.environ.get("MONGO_SERVER_HOST",9990)
username = os.environ.get("MONGO_USERNAME",9990)
password = os.environ.get("MONGO_PASSWORD",9990)

client = MongoClient(username=username, port=int(port), host=host, password=password)

@app.route('/')
def home():
    return f"Hello world!"
    
