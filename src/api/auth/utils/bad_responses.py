from fastapi import status

from src.core.schemas import BaseResponseModel


def account_exists_response(email: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Пользователь {email} уже зарегистрирован.'
    )


def account_confirmed_already(email: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Аккаунт {email} уже подтвержден.'
    )


def account_not_confirmed(email: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Аккаунт {email} не подтвержден.'
    )


def incorrect_email_or_ivite_token():
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный account или invite token.'
    )
