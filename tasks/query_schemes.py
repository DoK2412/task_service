from pydantic import BaseModel
from fastapi import Query


class PostTask(BaseModel):
    task_name: str = Query(description="Наименование задачи")
    description: str = Query(description="Текст задачи")
    status: bool = Query(description="Статус задачи")


class PutTask(BaseModel):
    id: int = Query(description="Id задачи")
    task_name: str = Query(default=None, description="Новое имя задачи")
    description: str = Query(default=None, description="Новое описание задачи")
    status: bool = Query(default=None, description="Статус задачи")