from pydantic import BaseModel


class BaseResponseModel:
    status_code: int
    error: bool
    payload: dict
