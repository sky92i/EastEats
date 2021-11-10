db.auth('comp3122', '12345')
db = db.getSiblingDB('EasyEats')

db.createCollection('order');
db.order.insertOne({'order_id':'1', 'current_state':'created', 'type':'pick_up'});
db.order.insertOne({'order_id':'2', 'current_state':'accepted', 'type':'dine_in'});
db.order.insertOne({'order_id':'3', 'current_state':'denied', 'type':'delievered_by_ee'});
db.order.insertOne({'order_id':'4', 'current_state':'finished', 'type':'delievered_by_store'});
db.order.insertOne({'order_id':'5', 'current_state':'canceled', 'type':'pick_up'});


db.createCollection('store');
db.store.insertOne({'store_id':'1', 'name':'Wally Waffles'});
db.store.insertOne({'store_id':'2', 'name':'Happy Hamburger'});
db.store.insertOne({'store_id':'3', 'name':'Lucid Lunch'});
db.store.insertOne({'store_id':'4', 'name': 'Arnold Acai'});
db.store.insertOne({'store_id':'5', 'name': 'Good Gouda'});


db.createCollection('store.status');
db.store.status.insertOne({'store_id':'1', 'status': 'OFFLINE', 'offlineReason': 'OUT_OF_MENU_HOURS'});
db.store.status.insertOne({'store_id':'2', 'status': 'ONLINE', 'offlineReason': 'Store is online'});
db.store.status.insertOne({'store_id':'3', 'status': 'OFFLINE', 'offlineReason': 'INVISIBLE'});
db.store.status.insertOne({'store_id':'4', 'status': 'OFFLINE', 'offlineReason': 'PAUSED_BY_UBER'});


db.createCollection('store.holiday');
db.store.holiday.insertOne({'store_id': '1', 'holiday_hours': {'2021-12-24': {'open_time_periods': [{'start_time': '08:00', 'end_time': '16:00'}]}, '2021-12-25': {'open_time_periods': [{'start_time': '00:00', 'end_time': '00:00'}]}}});
db.store.holiday.insertOne({'store_id': '2', 'holiday_hours': {}});
db.store.holiday.insertOne({'store_id': '3', 'holiday_hours': {'2021-12-25': {'open_time_periods': [{'start_time': '00:00', 'end_time': '00:00'}]}}});


db.createCollection('menu');
db.menu.insertOne({'store_id': '1', 'items': [{'item_id': 'Waffle', 'price': '100', 'available': 'yes'}, {'item_id': 'Chicken and waffle', 'price': '200', 'available': 'yes'}]});
db.menu.insertOne({'store_id': '2', 'items': [{'item_id': 'Hamburger', 'price': '150', 'available': 'yes'}, {'item_id': 'Cheeseburger', 'price': '180', 'available': 'yes'}]});
db.menu.insertOne({'store_id': '3', 'items': [{'item_id': 'Noodles', 'price': '80', 'available': 'no'}, {'item_id': 'Dumplings', 'price': '140', 'available': 'yes'}]});
db.menu.insertOne({'store_id': '4', 'items': [{'item_id': 'Smoothie', 'price': '40', 'available': 'yes'}, {'item_id': 'Bowl', 'price': '50', 'available': 'yes'}]});
