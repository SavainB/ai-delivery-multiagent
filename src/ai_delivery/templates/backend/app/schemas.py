from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
