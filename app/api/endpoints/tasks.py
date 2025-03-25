from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.models.database import get_db
from app.schemas import TaskRead, TaskCreate
from app.auth import get_current_user
from app.models.models import User
from app.schemas import tasks as schemas
from app.crud import tasks as crud

router = APIRouter()

# create a task
@router.post("/tasks/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

# get tasks
@router.get("/tasks/", response_model=List[schemas.TaskRead])
def get_task(db: Session = Depends(get_db)):
    tasks = crud.get_tasks_by_user(db=db, user_id = 1)
    if not tasks:
        raise HTTPException(status_code=404,detail="No task Found" )
    return tasks

# get a specific task
@router.get("/tasks/{task_id}", response_model = schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db = db, task_id = task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

# get all tasks for a user
@router.get("/tasks/", response_model=List[schemas.TaskRead])
def get_user_tasks(user_id: int, db: Session=Depends(get_db)):
    tasks = crud.get_tasks_by_user(db = db, user_id = user_id)
    if tasks:
        return {"message": f"All the tasks for user {user_id} are: {tasks}"}
    elif len(tasks) == 0:
        return {"message": f"There are no tasks for user {user_id}"}
    else:
        raise HTTPException(status_code=404, detail="ERROR: user and tasks not found")
    

# update a task    
@router.put("/tasks/{task_id}", response_model= schemas.TaskRead)
def update_task(task_id: int, task = schemas.TaskCreate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db=db, task_id = task_id, task_update = task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="task not found")
    return updated_task

# delete a task
@router.delete("/tasks/{tasks_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_to_delete = crud.get_task(db=db, task_id=task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    
    crud.delete_task(db=db, task_id=task_id)
    return {"message": f"Task '{task_to_delete.description} (ID: {task_to_delete.id}) deleted successfully"}

# update task status
@router.put("/tasks/{task_id}/status", response_model=schemas.TaskRead)
def update_task_status(task_id:int, status_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_task = crud.update_task_status(db=db, task_id=task_id, new_status=status_update)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task