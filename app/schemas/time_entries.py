from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimeEntryBase(BaseModel):
    task_id: int
    user_id: int
    
class TimeEntryCreate(TimeEntryBase):
    start_time: Optional[datetime] = None
    
class TimeEntryStop(BaseModel):
    end_time: datetime
    
class TimeEntryRead(TimeEntryBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True