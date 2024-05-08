from fastapi import status

from src.core.schemas import BaseResponseModel


def invalid_account_id(account_id: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный account_id {account_id}.'
    )
