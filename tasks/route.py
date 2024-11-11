from fastapi import APIRouter, Response, Request, Query

from .query_schemes import PostTask, PutTask
from .incoming_requests import crate_tasks, get_task, update_task, delete_task

router_tasks = APIRouter(prefix="/tasks")


@router_tasks.post("", tags=["tasks"])
async def create_task(request: Request,
                      task: PostTask):
    result = await crate_tasks(request, task)
    return result


@router_tasks.get("", tags=["tasks"])
async def get_tasks(request: Request,
                   status: bool = Query(None, description="Статус задачи")):
    result = await get_task(request, status)
    return result


@router_tasks.put("", tags=["tasks"])
async def put_tasks(request: Request,
                    task: PutTask):
    result = await update_task(request, task)
    return result


@router_tasks.delete("", tags=["tasks"])
async def delete_tasks(request: Request,
                       id: int = Query(description="Id задачи")):
    result = await delete_task(request, id)
    return result