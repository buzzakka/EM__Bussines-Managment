from fastapi import FastAPI

from src.api.auth.v1.middleware import AuthMiddleware
from src.api.auth.router import router as auth_router

app: FastAPI = FastAPI()

# routers
app.include_router(auth_router)

# middlewares
app.add_middleware(AuthMiddleware)
