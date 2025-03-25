from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    tasks = relationship("Task", back_populates="owner")
    time_entries = relationship("TimeEntry", back_populates="user")

class Task(Base):
    __tablename__= "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    isCompleted = Column(Boolean, default=False)
    due_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'))

    #One task belongs to one user
    owner = relationship("User", back_populates="tasks")
    #One task can have more than one time entry
    time_entries = relationship("TimeEntry", back_populates="task")

class TimeEntry(Base):
    __tablename__= "time_entries"
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    task_id = Column (Integer, ForeignKey('tasks.id'))
    user_id = Column (Integer, ForeignKey('users.id'))

    task = relationship("Task", back_populates="time_entries")
    user = relationship("User", back_populates="time_entries")
