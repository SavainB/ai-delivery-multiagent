from fastapi import APIRouter, HTTPException

from ..schemas import Task, TaskCreate
from ..services import create_task, delete_task, get_task, list_tasks, update_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[Task])
def list_all_tasks() -> list[dict]:
    return list_tasks()


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int) -> dict:
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=Task, status_code=201)
def create_new_task(payload: TaskCreate) -> dict:
    return create_task(payload.model_dump())


@router.put("/{task_id}", response_model=Task)
def update_existing_task(task_id: int, payload: TaskCreate) -> dict:
    task = update_task(task_id, payload.model_dump())
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_existing_task(task_id: int) -> None:
    deleted = delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
