
from sanic import Sanic, request
from sanic.response import html, json
from sanic_cors import CORS, cross_origin
from db import ChatFactory
import socketio
from sqlalchemy.exc import IntegrityError


mgr = socketio.AsyncRedisManager('redis://127.0.0.1:6379/1')
#sio = socketio.AsyncServer(client_manager=mgr, async_mode='sanic')
sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
CORS(app, automatic_options=True)
sio.attach(app)


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(5)
        count += 1
        await sio.emit('test', {'data': 'Server generated event:{}'.format(count)},
                       namespace='/test')


@app.listener('before_server_start')
def before_server_start(sanic, loop):
    sio.start_background_task(background_task)


@app.route('/')
async def index(request):
    with open('app.html') as f:
        return html(f.read())


@app.route('/rooms')
async def rooms(request):
    if not request.args:
        return json(ChatFactory().get_rooms())
    return json(ChatFactory().get_rooms_by_user_name(request.args['user_name'][0]))


@sio.on('my event', namespace='/test')
async def test_message(sid, message):
    await sio.emit('response', {'data': message['data']}, room=sid,
                   namespace='/test')


@sio.on('my broadcast event', namespace='/test')
async def test_broadcast_message(sid, message):
    await sio.emit('response', {'data': message['data']}, namespace='/test')


@sio.on('join', namespace='/test')
async def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/test')
    try:
        ChatFactory().add_room(room_name=message['room'], user='alistair@test')
    except IntegrityError:
        pass
    try:
        ChatFactory().add_user_room(room_name=message['room'], user_name='alistair@test')
    except IntegrityError as e:
        pass
    await sio.emit('rooms', {'data': 'Entered room: ' + message['room'], 'sid':sid},
                   room=sid, namespace='/test')


@sio.on('leave', namespace='/test')
async def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace='/test')
    await sio.emit('response', {'data': 'Left room: ' + message['room']},
                   room=sid, namespace='/test')


@sio.on('close room', namespace='/test')
async def close(sid, message):
    await sio.emit('response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'], namespace='/test')
    await sio.close_room(message['room'], namespace='/test')


@sio.on('room_event', namespace='/test')
async def send_room_message(sid, message):
    print(message)
    await sio.emit('response', {'data': message['data'], 'sid': sid, 'room': message['room']},
                   room=message['room'], namespace='/test')


@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    await sio.emit('response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


app.static('/static', './static')


if __name__ == '__main__':
    app.run(host='0.0.0.0')