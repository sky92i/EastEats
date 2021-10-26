db.auth('comp3122', '12345')
db = db.getSiblingDB('EasyEats')

db.createCollection('order');
db.student.insertOne({'order_id':'1', 'current_state':'created', 'type':'pick_up'});
db.student.insertOne({'order_id':'2', 'current_state':'accepted', 'type':'dine_in'});
db.student.insertOne({'order_id':'3', 'current_state':'denied', 'type':'delievered_by_ee'});
db.student.insertOne({'order_id':'4', 'current_state':'finished', 'type':'delievered_by_store'});
db.student.insertOne({'order_id':'5', 'current_state':'canceled', 'type':'pick_up'});


db.createCollection('store');
db.takes.insertOne({'store_id':'1', 'name':'Wally Waffles'});
db.takes.insertOne({'store_id':'2', 'name':'Happy Hamburger'});
db.takes.insertOne({'store_id':'3', 'name':'Lucid Lunch'});