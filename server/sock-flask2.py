import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template, jsonify, request
from db import ChatFactory
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

sio = socketio.Server(async_mode='eventlet')
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    if not request.args:
        return jsonify(ChatFactory().get_rooms())
    return jsonify(ChatFactory().get_rooms_by_user_name(request.args['user_name']))

@sio.on('connect', namespace='/test')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('join', namespace='/test')
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/test')
    try:
        ChatFactory().add_room(room_name=message['room'], user='alistair@test')
    except IntegrityError:
        pass
    try:
        ChatFactory().add_user_room(room_name=message['room'], user_name='alistair@test')
    except IntegrityError as e:
        pass
    sio.emit('rooms', {'data': 'Entered room: ' + message['room'], 'sid':sid},
                   room=sid, namespace='/test')

@sio.on('room_event', namespace='/test')
def send_room_message(sid, message):
    print(message)
    sio.emit('response', {'data': message['data'], 'sid': sid, 'room': message['room']},
                   room=message['room'], namespace='/test')

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)