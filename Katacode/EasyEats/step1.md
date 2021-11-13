# Setup the Docker-compose (Heading for Step 1)

Overview
Docker compose is a tool for defining and running multi-container Docker application.

In this section, we will use Docker compose to Build and Deploy a "EasyEats" which is available at
https://github.com/polyu21022574x/EasyEats

The app is composed of the following components:

Voting-App: Frontend of the application written in Python, used by users to cast their votes. Each vote cast on the Voting app is stored in the Redis in-memory database.

Result-App: Frontend of the application written in Node.js, displays the voting results.

Redis: In-memory database used as intermediate storage.

DB: PostgreSQL database used as database.

Worker: The .Net worker service fetches the vote and stores it in the Postgres DB, which is then accessed by the Node.js frontend.

Clone the project from github.
`git clone https://github.com/polyu21022574x/EasyEats'`{{execute}}

View the docker compose file for launching your application's services.
'docker-compose.yaml'