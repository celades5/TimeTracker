from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    task = relationship("Task", back_populates="owner")
    time_entries = relationship("TimeEntry", back_populates="user")

class Task(Base):
    __tablename__= 'tasks'   