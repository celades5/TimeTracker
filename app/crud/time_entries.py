from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.models import TimeEntry
from app.schemas.time_entries import TimeEntryCreate, TimeEntryStop

# Start tracking time
def start_time_entry(db:Session, time_entry: TimeEntryCreate):
    new_entry = TimeEntry(**time_entry.model_dump(), start_time=datetime.now(timezone.utc))
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# Stop time entry
def stop_time_entry(db:Session, time_entry_update: TimeEntryStop, entry_id: int):
    entry = db.query(TimeEntry).filter(TimeEntry.id == entry_id).first()
    if entry and not entry.end_time:
        entry.end_time = time_entry_update.end_time or datetime.now(timezone.utc)
        db.commit()
        db.refresh(entry)
        return entry
    
# get all time entries for a task
def get_time_entries_for_task(db:Session, task_id:int):
    return db.query(TimeEntry).filter(TimeEntry.id == task_id).all()