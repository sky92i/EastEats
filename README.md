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

/testwebhook/addorder
- will create a dummy order with order id 888

/testwebhook/cancelorder
- cancel the dummay order with order id 888

## Logging services

The project uses Prometheus and Grafana for logging.

Access prometheus at:
``` localhost:9090 ```

Access grafana at:
``` localhost:3000 ```
with username: admin and password: admin
