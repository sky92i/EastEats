# Setup the Docker-compose

## To run the code
Run the project with docker compose
`cd EasyEats`{{execute}}
`docker-compose up`{{execute}}

Access the API from localhost at port 9990
`curl localhost:9990`{{execute}}

## Authentication
The API is secured with Auth0 and Kong Gateway. To access the API, an access token is required when sending an request.

Example for getting an access token for the API:

We can execute a client credentials exchange to get an access token for easyeats.

`curl --request POST \--url https://sky92i.jp.auth0.com/oauth/token \--header 'content-type: application/json' \--data '{"client_id":"Nhh2ojJcgIHg0fh86dAuDJdWwEZ6aUit","client_secret":"A1kIo2nD9VTg45WBBHv5s_9eOPNSI-Vg1ZXVmj5cnz6i24LiWTIGYsuWjTOj-RqN","audience":"https://easyeats","grant_type":"client_credentials"}'`{{execute}}

***Response:***
```
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxGUmlMYi0ycHBUWFRzTC1QT3M2UCJ9.eyJpc3MiOiJodHRwczovL3NreTkyaS5qcC5hdXRoMC5jb20vIiwic3ViIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXRAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZWFzeWVhdHMiLCJpYXQiOjE2MzY1MzcxNzIsImV4cCI6MTYzNjYyMzU3MiwiYXpwIjoiTmhoMm9qSmNnSUhnMGZoODZkQXVESmRXd0VaNmFVaXQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.J2I9vGYbQ58FGbwxMCAy6M-BbDhmo_4untC0uNp8q1z3dG_eYRLJ211lJlx4rjFhCwTCJi5-3G_cyb6Tdt8lvpYpTz9TV5H0PvIemUs2crmvx3qohNHOOjNWqqja0_A09RuKUc-LaEJ8WzY-bKBxg_demsrRtAp6TJpiv38HcaWy3QxdWWEiPUVoZfSwpeQzYrsrxOsZ5ygFbXVFPrsIM1ensBYpdaAsIQ0nS7PTBS1c-AMg2cPDWlIyRm1Qt6qADv5beP0OUqHYFVAFTwC-MosJHPVQ9Y6FSpsQ51xYo5MTLWwreftk6gZfSo_B8P1TPWIvSAsEiiZwVz3SYY-k8Q",
  "token_type": "Bearer"
}
```



