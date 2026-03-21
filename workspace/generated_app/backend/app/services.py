from .db import TASKS


def list_tasks() -> list[dict]:
    return TASKS


def get_task(task_id: int) -> dict | None:
    return next((task for task in TASKS if task["id"] == task_id), None)


def create_task(payload: dict) -> dict:
    task = {"id": max((item["id"] for item in TASKS), default=0) + 1, **payload}
    TASKS.append(task)
    return task


def update_task(task_id: int, payload: dict) -> dict | None:
    task = get_task(task_id)
    if task is None:
        return None
    task.update(payload)
    return task


def delete_task(task_id: int) -> bool:
    task = get_task(task_id)
    if task is None:
        return False
    TASKS.remove(task)
    return True
