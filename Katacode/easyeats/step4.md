# Learn with different store endpoint

## Store endpoint

```[GET]``` localhost:8000/stores/<store_id>
- to see store information

```[GET]``` localhost:8000/stores
- to list all stores

```[GET]``` localhost:8000/stores/<store_id>/status
- to see the online status of a restaurant 

```[POST]``` localhost:8000/stores/<store_id>/status
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
- to see the holiday hours of a restaurant 

```[POST]``` localhost:8000/stores/<store_id>/holiday-hours
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

