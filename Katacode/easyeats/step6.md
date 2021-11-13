# Heading for Step 3

## Webhook Notifications
A webhook will be sent to a webhook listener when an order has been created or canceled.
In this case, a webhook listener is created for testing. The webhook is set to send to the webhook_listner container. Also, 2 endpoints created for creating or cancelling a dummy order for testing the webhook function.

Visit localhost:5001 at browser will start to listen the webhook and the received webhook will be parsed and displayed on the webpage.
Then, we can visit the following endpoints to send webhook and check the results on localhost:5001. The results should be displayed immediately without refreshing the webpage manually.

localhost:9990/testwebhook/addorder
- will create a dummy order with order id 888

localhost:9990/testwebhook/cancelorder
- cancel the dummay order with order id 888

## API gateway
Kong gateway is used for our API gateway. The config file is kong.yaml.
The web GUI can be visited at 
http://localhost:8002/default/dashboard

## Logging services

The project uses Prometheus and Grafana for logging.

Access prometheus at:
`localhost:9090`

Access grafana at:
`localhost:3000`
with 
- username: admin 
- password: admin
