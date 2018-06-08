from socketIO_client import SocketIO, BaseNamespace
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()


class Namespace(BaseNamespace):

	def on_my_response(self, *args):
		print('on_aaa_response', args)
		self.emit('bbb')

	def on_message(self, data):
		print('on_aaa_response', data)
		self.emit('bbb')
	def on_event(self, event, *args):
		print(event)

	def on_connect(self):
		print('[Connected]')

	def on_reconnect(self):
		print('[Reconnected]')

	def on_disconnect(self):
		print('[Disconnected]')
print('HI')
socketIO = SocketIO('127.0.0.1', 8000, transports='websockets')
print('HI')
chat_namespace = socketIO.define(Namespace, '/test', )
print('HI')
# Listen
# chat_namespace.on('my room event', on_aaa_response)
# chat_namespace.on('my response', on_aaa_response)
# chat_namespace.on('test', on_aaa_response)
# chat_namespace.emit('join', {'room':'alistair'})
# chat_namespace.emit('my room event',{'data':'test', "room":'alistair'})
socketIO.wait(seconds=1)





#socketIO = SocketIO('localhost', 8000, Namespace)

print('HI')
#socketIO.wait(seconds=1)