from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    description: str
    due_date: Optional[datetime] = None
    status: Optional[str] = "To Do"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    isCompleted: bool

class TaskRead(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True