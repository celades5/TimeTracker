from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.crud import analytics as crud
from app.auth import get_current_user
from app.models.models import User

router = APIRouter()

# get total time spent on tasks
@router.get("/tasks/{task_id}/total-time")
def get_total_time_for_task(task_id: int, db: Session= Depends(get_db), current_user: User= Depends(get_current_user)):
    total_time = crud.get_total_time_for_task(db=db, task_id=task_id)
    return {"task_id": task_id, "total time spent: ": total_time}

# get total time by user
@router.get("/users/{user_id}/total-time")
def get_totoal_time_for_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    total_time = crud.get_total_time_for_user(db=db, user_id=user_id)
    return {"user_id: ": user_id, "total time spent is: ": total_time}

# get completed tasks count
@router.get("/users/{user_id}/completed-tasks")
def get_completed_tasks(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    completed_tasks = crud.get_completed_taks_count(db=db, user_id=user_id)
    return {"user_id: ": user_id, "total completed tasks: ": completed_tasks}

# get average time for task
@router.get("/users/{user_id}/average-completion-time")
def get_average_completion_time(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    avg_time = crud.get_average_completion_time(db=db, user_id=user_id)
    return {"user_id ": user_id, "average task completed in: ": avg_time}

# get summary productivity
@router.get("/users/{user_id}/productivity-summary")
def get_productivity_summary(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    summary = crud.get_productivity_summary(db=db, user_id=user_id)
    return {"user_id: ": user_id, "productivuty summary: ": summary}