from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.schemas import time_entries as schemas
from app.crud import time_entries as crud
from app.models.database import get_db
from app.auth import get_current_user
from app.models.models import User, TimeEntry


router = APIRouter()

# start a time entry
@router.post("/tasks/{task_id}/start", response_model=schemas.TimeEntryRead)
def start_time_entry(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    time_entry_data = schemas.TimeEntryCreate(task_id=task_id, user_id=current_user.id)
    return crud.start_time_entry(db=db, time_entry=time_entry_data)

# Stop time entry
@router.put("/tasks/{task_id}/stop", response_model=schemas.TimeEntryRead)
def stop_time_entry(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    entry = db.query(TimeEntry).filter(
        TimeEntry.task_id == task_id,
        TimeEntry.user_id == current_user.id,
        TimeEntry.end_time.is_(None)
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="No active time entry found for this task")
    time_entry_update = schemas.TimeEntryStop(end_time=datetime.now(timezone.utc))
    return crud.stop_time_entry(db=db, entry_id=entry.id, time_entry_update=time_entry_update)

# Get time entries for a task
@router.get("/tasks/{task_id}/time-entries", response_model=List[schemas.TimeEntryRead])
def get_time_entreis(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_time_entries_for_task(db=db, task_id=task_id)