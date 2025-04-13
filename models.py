from sqlalchemy import Column, Integer, String, Time, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

meeting_user_association = Table(
    'meeting_user_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('meeting_id', Integer, ForeignKey('meetings.id'), primary_key=True)
)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    meetings = relationship("MeetingModel", secondary=meeting_user_association, back_populates="attendees")

class MeetingModel(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    time = Column(Time)
    content = Column(String)
    attendees = relationship("UserModel", secondary=meeting_user_association, back_populates="meetings")
