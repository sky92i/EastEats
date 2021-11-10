# EasyEats
Group project for course COMP3122

## To run the code

Run the project with docker compose <br /> 
```docker-compose up```

Access the API from localhost at port 9990 <br /> 
```curl localhost:9990```

## Authentication
The API is secured with [Auto0](https://auth0.com/). To access the API, an access token is required when sending an request.
\
\
Example for getting an access token for the API:

We can execute a client credentials exchange to get an access token for easyeats.
```
curl --request POST \
  --url https://sky92i.jp.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"Nhh2ojJcgIHg0fh86dAuDJdWwEZ6aUit","client_secret":"A1kIo2nD9VTg45WBBHv5s_9eOPNSI-Vg1ZXVmj5cnz6i24LiWTIGYsuWjTOj-RqN","audience":"https://easyeats","grant_type":"client_credentials"}'
```
Response:
```
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxGUmlMYi0ycHBUWFRzTC1QT3M2UCJ9.eyJpc3MiOiJodHRwczovL3NreTkyaS5qcC5hdXRoMC5jb20vIiwic3ViIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXRAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZWFzeWVhdHMiLCJpYXQiOjE2MzY1MzcxNzIsImV4cCI6MTYzNjYyMzU3MiwiYXpwIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.J2I9vGYbQ58FGbwxMCAy6M-BbDhmo_4untC0uNp8q1z3dG_eYRLJ211lJlx4rjFhCwTCJi5-3G_cyb6Tdt8lvpYpTz9TV5H0PvIemUs2crmvx3qohNHOOjNWqqja0_A09RuKUc-LaEJ8WzY-bKBxg_demsrRtAp6TJpiv38HcaWy3QxdWWEiPUVoZfSwpeQzYrsrxOsZ5ygFbXVFPrsIM1ensBYpdaAsIQ0nS7PTBS1c-AMg2cPDWlIyRm1Qt6qADv5beP0OUqHYFVAFTwC-MosJHPVQ9Y6FSpsQ51xYo5MTLWwreftk6gZfSo_B8P1TPWIvSAsEiiZwVz3SYY-k8Q",
  "token_type": "Bearer"
}
```
We can use the bearer token with an Authorization Header in our request to obtain authorized access to our API.
```
curl --request GET \
  --url http://localhost:9990/order/1 \
  --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxGUmlMYi0ycHBUWFRzTC1QT3M2UCJ9.eyJpc3MiOiJodHRwczovL3NreTkyaS5qcC5hdXRoMC5jb20vIiwic3ViIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXRAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZWFzeWVhdHMiLCJpYXQiOjE2MzY1MzU1MTMsImV4cCI6MTYzNjYyMTkxMywiYXpwIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.eGv526lXjcNERyhxlh43PLhZBfNyP5zKpmYHKqcxqqwQlxYJT67MV4Ck13sUUFFDqwQazVoXbGG2gId88Jj-J2iBuvYqK3T3AT_OPlSj0cuvlLl2981muqa3njwFXf2fdfemrobJaMNc-o2ZqgeLlkJb4gSG1WIk7LVC_IJkAfYFYPB9eeVC9Oq1YYu1kPsjQxUvsAecWYeC7EmE7q6GPzFT8MrtwJ_Xj9x9mHzo2X3N8rNeHcIxEp0sQRpeScPvjwPcbfKN58b_0FIrtju5ZOHwaEFjpiwF6XWdDDo6r_VU71q3nDUl79YjhkhTkL7tbtBY2kk8QREpRMxOvS8yyw'
```

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
