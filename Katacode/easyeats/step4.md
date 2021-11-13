# Learn with different store endpoint

```[GET]``` localhost:8000/stores/<store_id>

`curl localhost:8000/stores/1`{{execute}}

- to see store information

```[GET]``` localhost:8000/stores

`curl localhost:8000/stores`{{execute}}

- to list all stores

```[GET]``` localhost:8000/stores/<store_id>/status

`curl localhost:8000/stores/1/status`{{execute}}

- to see the online status of a restaurant 

```[POST]``` localhost:8000/stores/<store_id>/status

`curl localhost:8000/stores/1/status`{{execute}}

- to update the online status of a restaurant 
- must include JSON object with valid online status value and reason code value. Reason code needs to be valid if status is OFFLINE

***Request example:***
```
{
    "status": "OFFLINE", 
    "reason": "INVISIBLE"
}
```

```[GET]``` localhost:8000/stores/<store_id>/holiday-hours

`curl localhost:8000/stores/1/holiday-hours`{{execute}}

- to see the holiday hours of a restaurant 

```[POST]``` localhost:8000/stores/<store_id>/holiday-hours

`curl localhost:8000/stores/1/holiday-hours`{{execute}}

- to set the holiday hours of a restaurant
- must include JSON object with store id that exists in the store collection and holiday dates with opening hours
- if a store is closed the entire day, set start_time and end_time to 00:00 
- each call to this endpoint will overwrite any existing holiday hours

***Request example:***
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

