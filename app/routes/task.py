import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth, database

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Setup logger
logger = logging.getLogger("task_logger")
logging.basicConfig(level=logging.INFO)

# Redis client
redis_client = database.redis_client


# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Get All Tasks --------------------
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    cache_key = f"user:{current_user.id}:tasks"
    cached_tasks = redis_client.get(cache_key)

    if cached_tasks:
        logger.info("✅ Fetched tasks from Redis cache.")
        return json.loads(cached_tasks)

    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    tasks_data = [schemas.TaskResponse.from_orm(task).dict() for task in tasks]
    redis_client.set(cache_key, json.dumps(tasks_data), ex=300)  # Cache for 5 minutes

    logger.info("💾 Fetched tasks from DB and cached in Redis.")
    return tasks_data


# -------------------- Create a Task --------------------
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Invalidate cache
    redis_client.delete(f"user:{current_user.id}:tasks")
    logger.info("❌ Cache invalidated after task creation.")
    
    return new_task


# -------------------- Update a Task --------------------
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    # Invalidate cache
    redis_client.delete(f"user:{current_user.id}:tasks")
    logger.info("❌ Cache invalidated after task update.")

    return task


# -------------------- Delete a Task --------------------
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    
    db.delete(task)
    db.commit()

    # Invalidate cache
    redis_client.delete(f"user:{current_user.id}:tasks")
    logger.info("❌ Cache invalidated after task deletion.")

    return
