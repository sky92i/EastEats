# Learn with different order endpoint

## Order endpoint

[GET] localhost:8000/orders/<order_id>

- to see order details

[POST] localhost:8000/orders/<order_id>/accept_pos_order

- to accept order
- must include JSON object with reason value

***Request example:***

`{"reason": "accepted"}`

[POST] localhost:8000/orders/<order_id>/deny_pos_order

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

[POST] localhost:8000/orders/<order_id>/cancel

- to cancel order
- must include JSON object with cancel code and cancelling party

***Request example:***
```
{
	"reason":"cannot_complete_customer_note",
    "cancelling_party": "merchant"
}
```

[POST] localhost:8000/orders/<order_id>/restaurantdelivery/status

- to set delivery status
- must include JSON object with status

***Request example:***

`{"status": "delivered"}`