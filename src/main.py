from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer

from src.api.auth.router import router as auth_router

app: FastAPI = FastAPI()

app.include_router(auth_router)


# http_bearer = HTTPBearer()

# @app.middleware('http')
# async def check_authentication(request: Request, call_next):
#     token: str = await http_bearer(request)
#     print(token)
#     return await call_next(request)
