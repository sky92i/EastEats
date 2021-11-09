import pytest, requests

def test_get_specific_orders():
    response = requests.get("http://localhost:9990/order/1")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '1'
    assert response_body[0]["current_state"] == 'created'
    assert response_body[0]["type"] == 'pick_up'

    response = requests.get("http://localhost:9990/order/2")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '2'
    assert response_body[0]["current_state"] == 'accepted'
    assert response_body[0]["type"] == 'dine_in'

    response = requests.get("http://localhost:9990/order/3")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '3'
    assert response_body[0]["current_state"] == 'denied'
    assert response_body[0]["type"] == 'delievered_by_ee'

def test_accept_order():
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order", json={
        "reason": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason must be given'
    
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order", json={})
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order")
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order", json={
        "abcdefg": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order", json={
        "reason": "accepted"
    })
    assert response.status_code == 204
    
    response = requests.post("http://localhost:9990/orders/1/accept_pos_order", json={
        "reason": "accepted"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already accepted'



    response = requests.post("http://localhost:9990/orders/2/accept_pos_order", json={
        "reason": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason must be given'
    
    response = requests.post("http://localhost:9990/orders/2/accept_pos_order", json={})
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/2/accept_pos_order")
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/2/accept_pos_order", json={
        "abcdefg": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/2/accept_pos_order", json={
        "reason": "accepted"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already accepted'



    response = requests.post("http://localhost:9990/orders/123/accept_pos_order", json={
        "reason": "accepted"
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'order not found'

def test_deny_order():
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {}
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason must be given'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
            "explanation":"",
            "code":""
        }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason is not complete'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
		    "explanation":"failed to submit order"
	    }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
		    "code":"store_closed"
	    }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
            "explanation":"failed to submit order",
            "code":"1234"
	    }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason code invalid'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={})
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order")
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
            "explanation":"failed to submit order",
            "code":"store_closed"
	    }
    })
    assert response.status_code == 204
    
    response = requests.post("http://localhost:9990/orders/1/deny_pos_order", json={
        "reason": {
            "explanation":"failed to submit order",
            "code":"store_closed"
	    }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already denied'



    response = requests.post("http://localhost:9990/orders/3/deny_pos_order", json={
        "reason": {
            "explanation":"failed to submit order",
            "code":"store_closed"
	    }
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already denied'



    response = requests.post("http://localhost:9990/orders/123/deny_pos_order", json={
        "reason": {
            "explanation":"failed to submit order",
            "code":"store_closed"
	    }
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'order not found'

def test_cancel_order():
    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"",
        "cancelling_party": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason must be given'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'cancelling party must be given'
    
    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason must be given'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"abcdefg",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'reason code invalid'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": "abcdefg"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'invalid cancelling party'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={})
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/cancel")
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "abcdefg": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 204

    response = requests.post("http://localhost:9990/orders/1/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already canceled'



    response = requests.post("http://localhost:9990/orders/5/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'order is already canceled'



    response = requests.post("http://localhost:9990/orders/123/cancel", json={
        "reason":"cannot_complete_customer_note",
        "cancelling_party": "merchant"
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'order not found'

def test_update_delivery_status():
    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={
        "status": ""
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'Delivery status is not allowed'

    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={
        "status": "abcdefg"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'Delivery status is not allowed'

    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={
        "abcdefg": "abcdefg"
    })
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'
    
    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={})
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status")
    assert response.status_code == 400
    response_body = response.json()
    assert response_body["error"] == 'the format of given data is incorrect'

    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={
        "status": "arriving"
    })
    assert response.status_code == 204
    response = requests.post("http://localhost:9990/orders/1/restaurantdelivery/status", json={
        "status": "delivered"
    })
    assert response.status_code == 204


    response = requests.post("http://localhost:9990/orders/2/restaurantdelivery/status", json={
        "status": "arriving"
    })
    assert response.status_code == 204
    response = requests.post("http://localhost:9990/orders/2/restaurantdelivery/status", json={
        "status": "delivered"
    })
    assert response.status_code == 204


    response = requests.post("http://localhost:9990/orders/123/restaurantdelivery/status", json={
        "status": "delivered"
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'order not found'


def test_testwebhook_add_order():
    response = requests.get("http://localhost:9990/testwebhook/addorder")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 201
    response_body = response.json()
    assert response_body["Status"] == 'added order no. 888'

def test_testwebhook_cancel_order():
    response = requests.get("http://localhost:9990/testwebhook/cancelorder")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["Status"] == 'canceled order no. 888'

def test_error_404():
    response = requests.get("http://localhost:9990/abc")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'not found'

    response = requests.get("http://localhost:9990/order/12345")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["error"] == 'not found'

def test_error_405():
    response = requests.get("http://localhost:9990/orders/1/accept_pos_order")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 405
    response_body = response.json()
    assert response_body["error"] == 'method not allowed'

def test_get_specific_orders_again():
    response = requests.get("http://localhost:9990/order/1")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '1'
    assert response_body[0]["current_state"] == 'canceled'
    assert response_body[0]["type"] == 'pick_up'
    assert response_body[0]["status"] == 'delivered'

    response = requests.get("http://localhost:9990/order/2")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '2'
    assert response_body[0]["current_state"] == 'accepted'
    assert response_body[0]["type"] == 'dine_in'
    assert response_body[0]["status"] == 'delivered'

    response = requests.get("http://localhost:9990/order/3")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["order_id"] == '3'
    assert response_body[0]["current_state"] == 'denied'
    assert response_body[0]["type"] == 'delievered_by_ee'