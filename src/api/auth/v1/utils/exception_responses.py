from fastapi import status

from src.core.schemas import BaseResponseModel


def account_doesnt_exists_response(email: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Пользователь {email} уже зарегистрирован.'
    )
