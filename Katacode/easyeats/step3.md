# Learn with different order endpoint

```[GET]``` localhost:8000/orders/<order_id>

`curl localhost:8000/orders/1`{{execute}}

- to see order details

```[POST]``` localhost:8000/orders/<order_id>/accept_pos_order

`curl localhost:8000/orders/1/accept_pos_order`{{execute}}

- to accept order
- must include JSON object with reason value

***Request example:***

`{"reason": "accepted"}`

```[POST]``` localhost:8000/orders/<order_id>/deny_pos_order

`curl localhost:8000/orders/1/deny_pos_order`{{execute}}

- to deny order
- must include JSON object with reason value and reason code

***Request example:***
```
{
	"reason": {
		"explanation":"failed to submit order",
		"code":"store_closed"
	}
}
```

```[POST]``` localhost:8000/orders/<order_id>/cancel

`curl localhost:8000/orders/1/deny_pos_order`{{execute}}

- to cancel order
- must include JSON object with cancel code and cancelling party

***Request example:***
```
{
	"reason":"cannot_complete_customer_note",
    "cancelling_party": "merchant"
}
```

```[POST]``` localhost:8000/orders/<order_id>/restaurantdelivery/status

`curl localhost:8000/orders/1/restaurantdelivery/status`{{execute}}

- to set delivery status
- must include JSON object with status

***Request example:***

`{"status": "delivered"}`