# EasyEats
Group project for course COMP3122

## To run the code

Run the project with docker compose <br /> 
```docker-compose up```

Access the API from localhost at port 9990 <br /> 
```curl localhost:9990```

## Order endpoint
localhost:9990/order/<order_id>
- to see order details

localhost:9990/orders/<order_id>/accept_pos_order
- to accept order
- must include JSON object with reason value

localhost:9990/orders/<order_id>/deny_pos_order
- to deny order
- must include JSON object with reason value and reason code

localhost:9990/orders/<order_id>/cancel
- to cancel order
- must include JSON object with cancel code and cancelling party

localhost:9990/orders/<order_id>/restaurantdeliverystatus
- to set delivery status
- must include JSON object with status

## Logging services

The project uses Prometheus and Grafana for logging.

Access prometheus at:
``` localhost:9090 ```

Access grafana at:
``` localhost:3000 ```
with username: admin and password: admin
