import jwt

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from database.connection import JobDb
from database.sql_requests import *
from setting import SECRET_KEY, ALGORITHM
from log.logger import logger


async def crate_tasks(request: Request, task):
    try:
        payload = jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") and payload.get("user_name"):
            async with JobDb() as connector:
                check_task = await connector.fetch(CTEATE_TASK,
                                                   int(payload["user_id"]),
                                                   task.task_name,
                                                   task.description,
                                                   task.status)
                if check_task:
                    return JSONResponse(status_code=200, content={"detail": "Task created"})
                else:
                    raise HTTPException(status_code=422, detail="Server side error")
    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")


async def get_task(request: Request, status):
    try:
        payload = jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") and payload.get("user_name"):
            async with JobDb() as connector:
                get_all_task = await connector.fetch(GET_TASKS,
                                                     int(payload["user_id"]),
                                                     status, None)
                if get_all_task:
                    return get_all_task
                else:
                    return JSONResponse(status_code=200, content={"detail": "No task found"})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")


async def update_task(request: Request, task):
    try:
        payload = jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") and payload.get("user_name"):
            async with JobDb() as connector:
                update_user_task = await connector.fetch(UPDATE_TASK,
                                                         task.task_name,
                                                         task.description,
                                                         task.status,
                                                         int(payload["user_id"]),
                                                         task.id)
                if update_user_task:
                    return JSONResponse(status_code=200, content={"detail": "Task updated"})
                else:
                    return JSONResponse(status_code=200, content={"detail": "Task not found"})

    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")


async def delete_task(request, task_id):
    try:
        payload = jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") and payload.get("user_name"):
            async with JobDb() as connector:
                delete = await connector.fetch(DELETE_TASK,
                                          int(payload["user_id"]),
                                          task_id)

                check_task = await connector.fetch(GET_TASKS,
                                                   int(payload["user_id"]),
                                                   None,
                                                   task_id)
                if len(check_task) == len(delete):
                    return JSONResponse(status_code=200, content={"detail": "Task not found"})
                else:
                    return JSONResponse(status_code=200, content={"detail": "Task delete"})

    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")
