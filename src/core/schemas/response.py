from pydantic import BaseModel
from fastapi import status


class BaseResponseModel(BaseModel):
    status_code: int = status.HTTP_200_OK
    error: bool = False
    payload: dict | None = None
    message: str | None = None
