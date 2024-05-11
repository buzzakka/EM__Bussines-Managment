from typing import Any
from fastapi import status

from src.core.schemas import BaseResponseModel

def bad_param(name: str, value: Any, message: str = None):
    message: str = f'Неdерный параметр {name}: {value}.' if message is None else message
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=message
    )
