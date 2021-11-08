import json, uuid
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room

app = Flask(__name__)

REDIS_URL = 'redis://redis:6379'
socketio = SocketIO(app,logger=True,engineio_logger=True,message_queue=REDIS_URL)

@app.route("/", methods=['GET'])
def index():
    return render_template('webhooklistener.html')

def send_message(event, namespace, room, message):
    socketio.emit(event, message, namespace=namespace, room=room)

@app.before_first_request
def initialize_params():
    if not hasattr(app.config,'uid'):
        sid = str(uuid.uuid4())
        app.config['uid'] = sid

@app.route('/listenhooks', methods=['POST'])
def listenhooks():
    if request.method == 'POST':
        data = request.json
        if data:
           roomid =  app.config['uid']
           var = json.dumps(data)
           send_message(event='msg', namespace='/receivehooks', room=roomid, message=var)
    return 'OK'

@socketio.on('join_room', namespace='/receivehooks')
def on_room():
    if app.config['uid']:
        room = str(app.config['uid'])
        join_room(room)

if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0', port=5001,debug=True)