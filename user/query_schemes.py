from pydantic import BaseModel
from fastapi import Query


class Register(BaseModel):
    username: str = Query(description="Имя пользователя")
    password: str = Query(description="Пароль для автользации")
    confirm_pass: str = Query(description="Подтверждение пароля")


class Login(BaseModel):
    username: str = Query(description="Логин пользователя")
    password: str = Query(description="Пароль пользователя")

