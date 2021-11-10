import os, requests, json
from flask import Flask, jsonify, request, _request_ctx_stack
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt

AUTH0_DOMAIN = 'sky92i.jp.auth0.com'
API_AUDIENCE = 'https://easyeats'
ALGORITHMS = ["RS256"]

app = Flask(__name__)
metrics = PrometheusMetrics(app)
WEBHOOK_LISTENER_URL = 'http://webhook_listener:5001/listenhooks'

# Auth error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

try:
    # connect mongodb with the environment variables
    client = MongoClient(f'mongodb://{os.environ.get("MONGO_USERNAME")}:{os.environ.get("MONGO_PASSWORD")}@{os.environ.get("MONGO_SERVER_HOST")}:27017/{os.environ.get("MONGO_DATABASE")}?authSource=admin')
    client.server_info() # check database connection
    print ("[v] Database connection is successful.")
except Exception as e: # print error and exit
    print ("[x] Database connection error.")
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
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_order_details(order_id):
    data = [remove_id(i) for i in db.order.find({"order_id":order_id})]
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error":"not found"}), 404

@app.route('/orders/<order_id>/accept_pos_order', methods={'POST'})
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def accept_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        try:
            if request:
                request_body = request.json
                if not request_body["reason"]:
                    return jsonify({"error":"reason must be given"}), 400
            else:
                return jsonify({"error":"reason must be given"}), 400
        except KeyError:
            return jsonify({"error":"the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error":"the format of given data is incorrect"}), 400

        if data[0]['current_state'] == 'accepted':
            return jsonify({"error":"order is already accepted"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'accepted'}})
            return jsonify({}), 204
    return jsonify({"error":"order not found"}), 404

@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def deny_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        allowed_codes = ["store_closed","pos_not_ready","pos_offline","item_availability","missing_item","missing_info","pricing","capacity","address","special_instructions","other"]
        try:
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
        except KeyError:
            return jsonify({"error":"the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error":"the format of given data is incorrect"}), 400

        if data[0]['current_state'] == 'denied':
            return jsonify({"error":"order is already denied"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'denied'}})
            return jsonify({}), 204
    return jsonify({"error":"order not found"}), 404

@app.route('/orders/<order_id>/cancel', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def cancel_order(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        
        allowed_codes = ["out_of_items","kitchen_closed","customer_called_to_cancel","restaurant_too_busy","cannot_complete_customer_note","other"]
        allowed_parties = ["merchant", "customer"]
        try:
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
        except KeyError:
            return jsonify({"error":"the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error":"the format of given data is incorrect"}), 400

        if data[0]['current_state'] == 'canceled':
            return jsonify({"error":"order is already canceled"}), 400
        else:
            db.order.update_one({'order_id':order_id},{'$set':{'current_state':'canceled'}})
            send_webhook('cancel', order_id) # send webhook for canceled order
            return jsonify({}), 204
    return jsonify({"error":"order not found"}), 404

@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_delivery_status(order_id):
    cursor = db.order.find({'order_id':order_id})
    if cursor.count() > 0:
        request_body = request.json
        allowed_status = ["status","arriving","delivered"]
        try:
            if request_body["status"] not in allowed_status:
                return jsonify({"error":"Delivery status is not allowed"}), 400
            else:
                db.order.update_one({'order_id':order_id},{'$set':{'status':request_body["status"]}})
                return jsonify({}), 204
        except KeyError:
            return jsonify({"error":"the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error":"the format of given data is incorrect"}), 400
    return jsonify({"error":"order not found"}), 404

# for testing webhook when an order has been placed on the EasyEats
@app.route('/testwebhook/addorder', methods={'GET'})
def test_add_order():
    db.order.insert_one({'order_id':'888', 'current_state':'created', 'type':'pick_up'})
    send_webhook('add', 888)
    return jsonify({"Status": "added order no. 888"}), 201

# for testing webhook when an order has been cancelled by the Eater or EasyEats
@app.route('/testwebhook/cancelorder', methods={'GET'})
def test_cancel_order():
    db.order.update_one({'order_id': '888'},{'$set':{'current_state':'canceled'}})
    send_webhook('cancel', 888)
    return jsonify({"Status": "canceled order no. 888"}), 200

# send webhook to notify you that order has been placed or canceled
def send_webhook(action, order_id):
    if action == 'add':
        msg = {"event_type": "orders.notification", "order_id": order_id}
    elif action == 'cancel':
        msg = {"event_type": "orders.cancel", "order_id": order_id}

    requests.post(WEBHOOK_LISTENER_URL, data=json.dumps(
        msg, sort_keys=True, default=str), headers={'Content-Type': 'application/json'}, timeout=1.0)

# Retrieve existing store menu
@app.route('/stores/<store_id>/menus', methods=['GET'])
def get_menu(store_id):
    menu = db.menu.find_one({"store_id": store_id})
    if not menu:
        if not db.store.find_one({"store_id": store_id}):
            return jsonify({"error": "store not found"}), 404
        return jsonify({"error": "menu not found"}), 404
    return jsonify({"items": menu["items"]})

# Create or override the entire menu
@app.route('/stores/<store_id>/menus', methods=['PUT'])
def upload_menu(store_id):
    if not db.store.find_one({"store_id": store_id}):
        return jsonify({"error": "store not found"}), 404
    try:
        if request:
            request_body = request.json
            for item in request_body["items"]:
                if not (("item_id" in item) and ("price" in item) and ("available" in item)):
                    return jsonify({"error": "all items need to have an id, price and availability"}), 400
            if db.menu.find_one({"store_id": store_id}):
                db.menu.replace_one({"store_id": store_id}, {"store_id": store_id, "items": request_body["items"]})
                return jsonify({}), 204
            db.menu.insert_one({"store_id": store_id, "items": request_body["items"]})
            return jsonify({}), 204
    except KeyError:
        return jsonify({"error": "the format of given data is incorrect"}), 400
    except TypeError:
        return jsonify({"error": "the format of given data is incorrect"}), 400
    return jsonify({"error": "store x not found"}), 404

# Update an individual item within a store's menu
@app.route('/stores/<store_id>/menus/items/<item_id>', methods=['POST'])
def update_item(store_id, item_id):
    menu = db.menu.find_one({"store_id": store_id})
    if menu:
        item_id_exists = False
        for item in menu["items"]:
            if item["item_id"] == item_id:
                item_id_exists = True
        if not item_id_exists:
            return jsonify({"error": "the item_id does not exist"}), 404

        allowed_availability = ["yes", "no"]
        try:
            if request:
                request_body = request.json
                if "available" in request_body:
                    if request_body["available"] not in allowed_availability:
                        return jsonify({"error": f"availability keyword " + request_body["available"] + " is not allowed"}), 400
        except KeyError:
            return jsonify({"error": "the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error": "the format of given data is incorrect"}), 400

        request_body = request.json
        new_items = []
        if "available" in request_body:
            if "price" in request_body:
                for item in menu["items"]:
                    if item["item_id"] == item_id:
                        new_items.append({"item_id": item_id, "price": request_body["price"], "available": request_body["available"]})
                    else:
                        new_items.append({"item_id": item["item_id"], "price": item["price"], "available": item["available"]})
                db.menu.update_one({'store_id': store_id}, {'$set': {'items': new_items}})
                return jsonify({}), 204
            else:
                for item in menu["items"]:
                    if item["item_id"] == item_id:
                        new_items.append({"item_id": item_id, "price": item["price"], "available": request_body["available"]})
                    else:
                        new_items.append({"item_id": item["item_id"], "price": item["price"], "available": item["available"]})
                db.menu.update_one({'store_id': store_id}, {'$set': {'items': new_items}})
                return jsonify({}), 204
        if "price" in request_body:
            for item in menu["items"]:
                if item["item_id"] == item_id:
                    new_items.append({"item_id": item_id, "price": request_body["price"], "available": item["available"]})
                else:
                    new_items.append({"item_id": item["item_id"], "price": item["price"], "available": item["available"]})
            db.menu.update_one({'store_id': store_id}, {'$set': {'items': new_items}})
            return jsonify({}), 204
        else:
            return jsonify({"error": "the format of given data is incorrect"}), 400
    return jsonify({"error": "store's menu not found"}), 404

# Retrieve store information
@app.route('/stores/<store_id>', methods=['GET'])
def get_store_details(store_id):
    store = [remove_id(i) for i in db.store.find({"store_id": store_id})]
    if store:
        return jsonify(store[0]), 200
    else:
        return jsonify({"error": "not found"}), 404

# Retrieve all stores
@app.route('/stores', methods=['GET'])
def get_all_stores():
    stores = []
    for store in db.store.find():
        stores.append({"name": store["name"], "store_id": store["store_id"]})
    if not stores:
        return jsonify({"error": "not found"}), 404
    return jsonify(stores), 200

# Retrieve store online status availability
@app.route('/store/<store_id>/status', methods=['GET'])
def get_restaurant_status(store_id):
    query = db.store.status.find_one({"store_id": store_id})
    if not query:
        return jsonify({"error": "not found"}), 404
    return jsonify({"status": query["status"], "offlineReason": query["offlineReason"]})

# Set store online status availability
@app.route('/store/<store_id>/status', methods=['POST'])
def set_restaurant_status(store_id):
    cursor = db.store.status.find({'store_id': store_id})
    if cursor.count() > 0:
        data = [remove_id(i) for i in cursor]
        allowed_status = ["ONLINE", "PAUSED", "OFFLINE"]
        allowed_offline_reasons = ["OUT_OF_MENU_HOURS", "INVISIBLE", "PAUSED_BY_UBER", "PAUSED_BY_RESTAURANT"]
        try:
            if request:
                request_body = request.json
                if request_body["status"] not in allowed_status:
                    return jsonify({"error": f"restaurant status " + request_body["status"] + " is not allowed"}), 400
                if request_body["status"] != 'ONLINE' and request_body["reason"] not in allowed_offline_reasons:
                    return jsonify({"error": "must provide a valid offline reason"}), 400
                if not request_body["reason"]:
                    return jsonify({"error": "reason must be given"}), 400
                if not request_body["status"]:
                    return jsonify({"error": "status must be given"}), 400
            else:
                return jsonify({"error": "both status and reason must be given"}), 400
        except KeyError:
            return jsonify({"error": "the format of given data is incorrect"}), 400
        except TypeError:
            return jsonify({"error": "the format of given data is incorrect"}), 400

        if data[0]['status'] == request_body["status"]:         # If the new status is the same as the current one
            return jsonify({"error": f"restaurant status is already " + request_body["status"]}), 400
        else:
            db.store.status.update_one({'store_id': store_id}, {'$set': {'status': request_body["status"], 'offlineReason': request_body["reason"]}})
            return jsonify({}), 204
    return jsonify({"error": "store not found"}), 404

# Retrieve date-specific store hours
@app.route('/stores/<store_id>/holiday-hours', methods=['GET'])
def get_holiday_hours(store_id):
    query = db.store.holiday.find_one({"store_id": store_id})
    if not query:
        return jsonify({"error": "store not found"}), 404
    return jsonify({"holiday_hours": query["holiday_hours"]})

# Set date-specific store hours
@app.route('/stores/<store_id>/holiday-hours', methods=['POST'])
def set_holiday_hours(store_id):
    if not db.store.find_one({"store_id": store_id}):
        return jsonify({"error": "store not found"}), 404
    try:
        if request:
            request_body = request.json
            if db.store.holiday.find_one({"store_id": store_id}):
                db.store.holiday.replace_one({"store_id": store_id}, {"store_id": store_id, "holiday_hours": request_body["holiday_hours"]})
                return jsonify({}), 204
            db.store.holiday.insert_one({"store_id": store_id, "holiday_hours": request_body["holiday_hours"]})
            return jsonify({}), 204
    except KeyError:
        return jsonify({"error": "the format of given data is incorrect"}), 400
    except TypeError:
        return jsonify({"error": "the format of given data is incorrect"}), 400
    return jsonify({"error": "store holiday-hours not found"}), 404

# 404 error handler
@app.errorhandler(404)
def not_found(e):
    return {"error": "not found"}, 404

# 400 error handler
@app.errorhandler(400)
def bad_request(e):
    return {"error": "bad request"}, 400

# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    return {"error": "method not allowed"}, 405

# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return {"error": "internal server error"}, 500

#start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)