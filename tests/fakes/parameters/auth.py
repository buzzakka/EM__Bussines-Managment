from contextlib import nullcontext as does_not_raise
from fastapi import status

from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
    SignUpRequestSchema,
    SignUpResponseSchema,
)


TEST_ENDPOINT_CHECK_ACCOUNT: list[tuple[any]] = [
    (
        'example@user.ru',
        CheckAccountResponseSchema(account='example@user.ru').model_dump(),
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

TEST_ENDPOINT_SIGN_UP: list[tuple[any]] = [
    (
        SignUpRequestSchema(account='user_1@example.com', invite_token='123456').model_dump_json(),
        SignUpResponseSchema(account='user_1@example.com').model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        SignUpRequestSchema(account='user_3@example.com', invite_token='123456').model_dump_json(),
        {'detail': 'Пользователь уже зарегистрирован.'},
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    (
        SignUpRequestSchema(account='user_2@example.com', invite_token='000000').model_dump_json(),
        {'detail': 'Неверный адрес электронной почты или токен.'},
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    (
        SignUpRequestSchema(account='error@example.com', invite_token='000000').model_dump_json(),
        {'detail': 'Неверный адрес электронной почты или токен.'},
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPLETE: list[tuple[any]] = [
        
]
