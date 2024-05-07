from contextlib import nullcontext as does_not_raise
from fastapi import status

from src.api.auth.schemas.mixins import EmailSchema
from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
    
    SignUpRequestSchema,
    SignUpResponseSchema,
)


TEST_ENDPOINT_CHECK_ACCOUNT: list[tuple[any]] = [
    # Проверка аккаунта нового пользователя
    (
        'user@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(email='user@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    #Проверка аккаунта у пользователя, который уже проверял его
    (
        'user1@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(email='user1@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    #Проверка аккаунта у пользователя, который уже подтвердил его
    (
        'user3@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(email='user3@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    #Проверка аккаунта у зарегестрированного пользователя
    (
        'user2@example.com',
        CheckAccountResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user2@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPANY: list[tuple[any]] = [
    # Подтверждение корректного инвайт токена
    (
        SignUpRequestSchema(
            account='user4@example.com',
            invite_token='222222'
        ).model_dump(),
        SignUpResponseSchema(
            payload=EmailSchema(email='user4@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Подтверждение некорректного инвайт токена
    (
        SignUpRequestSchema(
            account='user@example.com',invite_token='qwerty'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный account или invite token.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Подтверждение с некорректной почты
    (
        SignUpRequestSchema(
            account='qwe@qwe.qwe',invite_token='qwerty'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный account или invite token.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Подтверждение уже подтвержденного аккаунта
    (
        SignUpRequestSchema(
            account='user4@example.com',invite_token='222222'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт user4@example.com уже подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Подтверждение уже зарегестрированного аккаунта
    (
        SignUpRequestSchema(
            account='user2@example.com',invite_token='222222'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user2@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPLETE_COMPANY: list[tuple[any]] = [
    
]
