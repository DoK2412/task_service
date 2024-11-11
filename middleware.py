from redis_class.connection import Redis

from fastapi.responses import JSONResponse


class SessionMiddleware(object):

    def __init__(self, request, call_next):
        self.request = request
        self.call_next = call_next

    async def session_check(self):
        if self.request.headers.get('Authorization'):
            async with Redis().redis as r:
                user_session = await r.get(self.request.cookies.get("user_id"))
            if user_session:
                if user_session.decode() == self.request.headers['Authorization'].split('Bearer ')[1]:
                    response = await self.call_next(self.request)
                    return response
                else:
                    return JSONResponse(content={"detail": "Passkey is not active"})
            else:
                return JSONResponse(content={"detail": "Passkey is not active"})
        else:
            return JSONResponse(content={"detail": "Authorization token is missing"})

