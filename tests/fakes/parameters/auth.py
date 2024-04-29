from contextlib import nullcontext as does_not_raise
from fastapi import status, HTTPException
import pytest

from src.api.auth.v1.schemas import CheckAccountResponseSchema


TEST_ENDPOINT_CHECK_ACCOUNT: list[tuple[any]] = [
    (
        'example@user.ru',
        CheckAccountResponseSchema(account='example@user.ru').model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        'user_1@example.com',
        CheckAccountResponseSchema(account='user_1@example.com').model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        'user_2@example.com',
        CheckAccountResponseSchema(account='user_2@example.com').model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        'user_3@example.com',
        {'detail': 'Пользователь уже зарегистрирован.'},
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]