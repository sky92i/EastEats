# Learn with different menu endpoint

```[GET]``` localhost:8000/stores/<store_id>/menus

`curl localhost:8000/stores/1/menus`{{execute}}

- to see the menu of a specific store

```[PUT]``` localhost:8000/stores/<store_id>/menus

`curl localhost:8000/stores/5/menus`{{execute}}

- to create or override the entire menu of a specific store
- every item on the menu needs to have an id, a price and an availability 

***Request example:***
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

```[POST]``` localhost:8000/stores/<store_id>/menus/items/<item_id>

`curl localhost:8000/stores/1/menus/items/1`{{execute}}

- to update information about an existing item on a store's menu
- will only update a field if it is specified in the request

***Request example 1:*** 
```
{ 
    "price": "120",
    "available": "no"
}
```

***Request example 2: ***
```
{
    "price": "75"
}
```
