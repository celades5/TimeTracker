from sqlalchemy.orm import Session
from app.models import models
from app.models.models import Task
from app.schemas.tasks import TaskCreate
from fastapi import HTTPException


# create task
def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), owner_id = user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# get task by id
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

# get all tasks by user
def get_tasks_by_user(db: Session, user_id: int):
    return (
        db.query(Task).filter(Task.owner_id == user_id).all()
    )

# update task
def update_task(db: Session, task_id: int, task_update: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task_update.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        raise HTTPException(status_code=404, detail=f"task with id {task_id} not found")
    
# detele task
def delete_task(db:Session, task_id: int, ):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        task_description = db_task.description
        db.delete(db_task)
        db.commit()
        return {"message": f"task with id {task_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"task with id {task_id} and description: {task_description}")
    
# update status of a task
def update_task_status(db: Session, task_id: int, new_status: str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.status = new_status
        if new_status.lower() == "done":
            task.isCompleted = True
        else:
            task.isCompleted = False
        
        db.commit()
        db.refresh(task)
        
    return task