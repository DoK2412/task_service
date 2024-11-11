import jwt


from fastapi import Response, HTTPException
from fastapi.responses import JSONResponse


from passlib.context import CryptContext
from datetime import datetime, timedelta


from setting import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from database.connection import JobDb
from database.sql_requests import *
from redis_class.connection import Redis
from log.logger import logger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password):
    """
    Функция хеширование пароля
    :param password: Пароль пользователя
    :return: Хеш пароля
    """
    return pwd_context.hash(password)


async def verify_password(password, hashed_password):
    """
    :param password: Пароль пользователя
    :param hashed_password: Хеш пароля пользователя из базы данных
    :return: Bool значение проверки паролей
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Функция создания токена
    :param data: информация загруженная в токен
    :param expires_delta: срок истечения действия токена доступа
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        # если срок есть используем его
        expire = datetime.utcnow() + expires_delta
    else:
        # если нет создаем на 15 минут
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def create_cookie(response: Response, user_id: int, user_name: str):
    """
    Функция добавления в сессию пользовательских данных
    :param response: параметры нагрузки запроса
    :param user_id: id пользователя
    :param user_name: имя пользователя
    :return:
    """
    response.set_cookie(key="user_id", value=str(user_id), samesite=None, secure=False)
    response.set_cookie(key="user_name", value=user_name, samesite=None, secure=False)


async def register_user(user):
    try:
        if user.password == user.confirm_pass:
            async with JobDb() as connector:
                check_user = await connector.fetch(CHER_USER, user.username)
                if check_user:
                    return JSONResponse(status_code=422, content={"detail": "Username already registered"})
                else:
                    password_hash = await get_password_hash(user.password)
                    create_user = await connector.fetch(CREATE_USER, user.username, password_hash)
                    if create_user:
                        return JSONResponse(content={"detail": "User registered"})
                    else:
                        return JSONResponse(status_code=422, content={"detail": "Server side error"})
        else:
            return JSONResponse(status_code=400, content={"detail": "User passwords do not match"})

    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")


async def login_user(response, request, user):
    try:
        async with JobDb() as connector:
            check_user = await connector.fetchrow(CHER_USER, user.username)
            if check_user and await verify_password(user.password, check_user["password_hash"]):
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(data={"user_id": check_user["id"], "user_name": check_user["username"]},
                                                   expires_delta=access_token_expires)
                await create_cookie(response, check_user["id"], check_user["username"])
                async with Redis().redis as r:
                    await r.setex(check_user["id"], 600, access_token)
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                return JSONResponse(status_code=400, content={"detail": "Incorrect username or password"})
    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")


async def refresh_tokens(request):
    try:
        if request.headers.get("Authorization"):
            try:
                payload = jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=[ALGORITHM])
                if payload.get("user_id") is None and payload.get("user_name") in None:
                    return JSONResponse(status_code=400, content={"detail": "Token invalid"})
                else:
                    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                    new_access_token = create_access_token(
                        data={"user_id": request.cookies["user_id"], "user_name": request.cookies["user_name"]},
                        expires_delta=access_token_expires)
                    return {"access_token": new_access_token, "token_type": "bearer"}
            except jwt.exceptions.ExpiredSignatureError:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                new_access_token = create_access_token(
                    data={"user_id": request.cookies["user_id"], "user_name": request.cookies["user_name"]},
                    expires_delta=access_token_expires)
                return {"access_token": new_access_token, "token_type": "bearer"}
            except jwt.exceptions.DecodeError:
                return JSONResponse(content={"detail": "Token invalid"})
        else:
            return JSONResponse(content={"detail": "Access to the service is denied"})

    except Exception as e:
        logger.exception(f"Ошибка при исполнении кода {e}")
        raise HTTPException(status_code=422, detail="Server side error")

