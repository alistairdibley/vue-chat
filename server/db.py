import datetime as dt
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text
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
    
    def add_room(self, room_name, user):
        room = Room(name=room_name, owner = user)
        self.session.add(room)
        self.session.commit()
        # return {'name':room.name, 'created':room.created_date, 'owner':room.owner}
    
    def add_user(self, user):
        user = User(name=user)
        self.session.add(user)
        self.session.commit()

    def get_rooms(self, all=False):
        print(self.session.query(Room).all())


if __name__ in '__main__':
   # Base.metadata.create_all(engine)

   cf = ChatFactory()
   cf.add_user('alistair@test')
   
