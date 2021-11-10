# EasyEats
Group project for course COMP3122

## To run the code

Run the project with docker compose <br /> 
```docker-compose up```

Access the API from localhost at port 9990 <br /> 
```curl localhost:9990```

## Order endpoint
```[GET]``` localhost:9990/order/<order_id>
- to see order details

\
```[POST]``` localhost:9990/orders/<order_id>/accept_pos_order
- to accept order
- must include JSON object with reason value

Request example:
```
{"reason": "accepted"}
```
\
```[POST]``` localhost:9990/orders/<order_id>/deny_pos_order
- to deny order
- must include JSON object with reason value and reason code

Request example:
```
{
	"reason": {
		"explanation":"failed to submit order",
		"code":"store_closed"
	}
}
```
\
```[POST]``` localhost:9990/orders/<order_id>/cancel
- to cancel order
- must include JSON object with cancel code and cancelling party

Request example:
```
{
	"reason":"cannot_complete_customer_note",
    "cancelling_party": "merchant"
}
```
\
```[POST]``` localhost:9990/orders/<order_id>/restaurantdelivery/status
- to set delivery status
- must include JSON object with status

Request example:
```
{"status": "delivered"}
```

## Webhook Notifications
A webhook will be sent to a webhook listener when an order has been created or canceled.
In this case, a webhook listener is created for testing. The webhook is set to send to the webhook_listner container. Also, 2 endpoints created for creating or cancelling a dummy order for testing the webhook function.

Visit localhost:5001 at browser will start to listen the webhook and the received webhook will be parsed and displayed on the webpage.
Then, we can visit the following endpoints to send webhook and check the results on localhost:5001. The results should be displayed immediately without refreshing the webpage manually.

localhost:9990/testwebhook/addorder
- will create a dummy order with order id 888

localhost:9990/testwebhook/cancelorder
- cancel the dummay order with order id 888

## Logging services

The project uses Prometheus and Grafana for logging.

Access prometheus at:
``` localhost:9090 ```

Access grafana at:
``` localhost:3000 ```
with username: admin and password: admin

## Store endpoint
```[GET]``` localhost:9990/stores/<store_id>
- to see store information

\
```[GET]``` localhost:9990/stores
- to list all stores

\
```[GET]``` localhost:9990/store/<store_id>/status
- to see the online status of a restaurant 

\
```[POST]``` localhost:9990/store/<store_id>/status
- to update the online status of a restaurant 
- must include JSON object with valid online status value and reason code value. Reason code needs to be valid if status is OFFLINE

Request example:
```
{
    "status": "OFFLINE", 
    "reason": "INVISIBLE"
}
```

\
```[GET]``` localhost:9990/stores/<store_id>/holiday-hours
- to see the holiday hours of a restaurant 

\
```[POST]``` localhost:9990/stores/<store_id>/holiday-hours
- to set the holiday hours of a restaurant
- must include JSON object with store id that exists in the store collection and holiday dates with opening hours
- if a store is closed the entire day, set start_time and end_time to 00:00 
- each call to this endpoint will overwrite any existing holiday hours

Request example: 
```
{
    "holiday_hours": 
        {"2021-12-24": {
            "open_time_periods": [
                {
                    "start_time": "08:00", 
                    "end_time": "16:00"
                }
            ]
        }, 
        "2021-12-25": {
            "open_time_periods": [
                {
                "start_time": "00:00", 
                "end_time": "00:00"
                }
            ]
        }
    }
}
```

## Menu endpoint
```[GET]``` localhost:9990/stores/<store_id>/menus
- to see the menu of a specific store

\
```[PUT]``` localhost:9990/stores/<store_id>/menus
- to create or override the entire menu of a specific store
- every item on the menu needs to have an id, a price and an availability 

Request example:
```
{
    "items": [
        {
            "available": "yes",
            "item_id": "Cracker",
            "price": "100"
        }, 
        {
            "available": "yes",
            "item_id": "Biscuit",
            "price": "200"
        }, 
        {
            "item_id": "Noodles", 
            "price": "80", 
            "available": "no"
        }
    ]
}
```

\
```[POST]``` localhost:9990/stores/<store_id>/menus/items/<item_id>
- to update information about an existing item on a store's menu
- will only update a field if it is specified in the request

Request example 1: 
```
{ 
    "price": "120",
    "available": "no"
}
```

Request example 2: 
```
{
    "price": "75"
}
```