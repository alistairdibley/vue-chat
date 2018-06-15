import datetime as dt
from collections import OrderedDict
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text, 
    PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///chat.db')
DBSession = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'user'
    name = Column(String(50), primary_key=True)

class Room(Base):
    __tablename__ = 'room'
    name = Column(String(50), primary_key=True)
    created_date = Column(DateTime, default=dt.datetime.utcnow())
    owner = Column(String(50), ForeignKey('user.name'))

class UserRoom(Base):
    __tablename__ = 'user_room'
    room_name = Column(String(50), ForeignKey('room.name'), primary_key=True)
    user_name = Column(String(50), ForeignKey('user.name'), primary_key=True)
    owner = Column(String(50), ForeignKey('user.name'))

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    user = Column(String(50), ForeignKey('user.name'))
    created_date = Column(DateTime, default=dt.datetime.utcnow())
    room = Column(String(50), ForeignKey('room.name'))

class ChatFactory(object):

    def __init__(self):
        self.session = DBSession()
    
    @staticmethod
    def _serialisation(model):
        columns = model.__mapper__.c.keys()
        result = OrderedDict()
        for key in columns:
             if isinstance(getattr(model, key), dt.datetime):
                 result[key] = str(getattr(model, key))
             else:
                 result[key] = getattr(model, key)
        return result

    def add_room(self, room_name, user):
        room = Room(name=room_name, owner = user)
        self.session.add(room)
        self.session.commit()
        return self._serialisation(room)
    
    def add_user_room(self, room_name, user_name):
        user_room = UserRoom(room_name=room_name, user_name=user_name)
        self.session.add(user_room)
        self.session.commit()

    def add_user(self, user):
        user = User(name=user)
        self.session.add(user)
        self.session.commit()
        return self._serialisation(user)
    
    def add_message(self, message, user, room):
        message = Message(content=message, user=user, room=room)
        self.session.add(message)
        self.session.commit()
        return self._serialisation(message)
        
    def get_rooms(self, all=False):
        return [self._serialisation(r) for r in self.session.query(Room).all()]
    
    def get_rooms_by_user_name(self, user_name):
        return [self._serialisation(r) for r in self.session.query(Room).join(UserRoom).filter(UserRoom.user_name == user_name).all()]
    
    def get_users(self, all=False):
        return [self._serialisation(r) for r in self.session.query(User).all()]

    def get_messages_by_room(self, room):
        return [self._serialisation(r) for r in self.session.query(Message).filter(Message.room == room).all()]


if __name__ in '__main__':
   Base.metadata.create_all(engine)

   cf = ChatFactory()
   print(cf.get_rooms('alistair@test'))
   
