# Overview of EasyEats

Overview
Docker compose is a tool for defining and running multi-container Docker application.

In this section, we will use Docker compose to Build and Deploy a "EasyEats" which is available at
https://github.com/polyu21022574x/EasyEats

The app is composed of the following components:

1. **Katacode:** Katacoda scenario

2. **grafana/provisioning:** Saving the dashboards and datasources

3. **orderapi:** Order API of the application written in Python, used by users to order.

4. **storeapi:** Store API of the application written in Python, used by users to order.

5. **tests:** unit.py makes use of pytest for unit testing the various endpoints of REST API

6. **webhook_listener:** Webhook will be sent to a webhook listener when an order has been created or canceled.

7. **README.md:** Detail of the application

8. **docker-compose.yaml:** docker compose file for launching the application's services

9. **mongo-init_order.js:** mongodb file for order

10. **mongo-init_store.js:** mongodb file for store

11. **prometheus.yml:** prometheus file for launching the prometheus services

Clone the project from github.
`git clone https://github.com/polyu21022574x/EasyEats`{{execute}}

View the docker compose file for launching your application's services.
`docker-compose.yaml`{{open}}