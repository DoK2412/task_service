import path as p


from fastapi import APIRouter, Response, Request, Query, Depends


from user.incoming_requests import register_user, login_user, refresh_tokens
from .query_schemes import Login, Register

router_user = APIRouter(prefix="/auth")


@router_user.post(p.REGISTER, tags=["auth"])
async def register(user: Register):
    result = await register_user(user)
    return result


@router_user.post(p.LOGIN, tags=["auth"])
async def login(response: Response,
                request: Request,
                user: Login):
    result = await login_user(response, request, user)
    return result


@router_user.post(p.REFRESH, tags=["auth"])
async def refresh_token(request: Request):
    result = await refresh_tokens(request)
    return result

