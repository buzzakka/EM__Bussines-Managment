from fastapi import FastAPI

from src.api.auth.v1.utils.middleware import AuthMiddleware
from src.api.router import router

app: FastAPI = FastAPI()

# routers
app.include_router(router)

# middlewares
app.add_middleware(AuthMiddleware, router=router)
