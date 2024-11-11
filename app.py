import uvicorn


from fastapi import FastAPI, Request

from contextlib import asynccontextmanager


from database.connection import JobDb
from tasks.route import router_tasks
from user.route import router_user
from middleware import SessionMiddleware
from setting import IGNOR_PATH
from redis_class.connection import Redis
from database.sql_requests import USER_TABLE, TASK_TABLE


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Ping successful Redis: {await Redis().redis.ping()}")
    await JobDb().create_pool()
    async with JobDb() as pool:
        await pool.execute(USER_TABLE)
        await pool.execute(TASK_TABLE)
    yield
    await JobDb().close_pool()


app = FastAPI(lifespan=lifespan)
app.include_router(router_tasks)
app.include_router(router_user)


@app.middleware("http")
async def add_headers(request: Request, call_next):
    if request.url.path in IGNOR_PATH:
        response = await call_next(request)
        return response
    else:
        session = await SessionMiddleware(request, call_next).session_check()
        return session

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8082, log_level="info")



