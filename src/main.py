from fastapi import FastAPI

from src.api.auth.router import router as auth_router

app: FastAPI = FastAPI()

app.include_router(auth_router)
