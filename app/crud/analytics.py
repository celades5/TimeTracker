from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.models import TimeEntry, Task
from datetime import datetime, timezone

# total time spend on task
def get_total_time_for_task(db: Session, task_id: int):
    total_time = (
        db.query(func.sum(func.extract("epoch", TimeEntry.end_time - TimeEntry.start_time)))
        .filter(TimeEntry.task_id == task_id, TimeEntry.end_time.isnot(None))
        .scalar()
    )
    return total_time if total_time else 0

# total time tracked by user
def get_total_time_for_user(db:Session, user_id: int):
    total_time = (
        db.query(func.sum(func.extract("epoch", TimeEntry.end_time - TimeEntry.start_time)))
        .filter(TimeEntry.user_id == user_id, TimeEntry.end_time.isnot(None))
        .scalar()
    )
    return total_time if total_time else 0

# count of completed tasks for user
def get_completed_taks_count(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id, Task.isCompleted == True).count()

# Average time to complete task
def get_average_completion_time(db: Session, user_id: int):
    completion_time = (
        db.query(func.avg(func.extract("epoch", Task.due_date - TimeEntry.start_time)))
        .join(TimeEntry, TimeEntry.task_id == Task.id)
        .filter(Task.owner_id == user_id, Task.isCompleted == True)
        .scalar()
    )
    return completion_time if completion_time else 0

# productivity summary for user
def get_productivity_summary(db: Session, user_id: int):
    total_time = get_total_time_for_user(db, user_id)
    completed_tasks = get_completed_taks_count(db, user_id)
    avg_completion_time = get_average_completion_time(db, user_id)
    
    return {
        "Total time spent: ": total_time,
        "Number of completed tasks ": completed_tasks,
        "Average time spent on tasks ": avg_completion_time
        
    }
