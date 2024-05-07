from contextlib import nullcontext as does_not_raise
from fastapi import status

from src.api.auth.schemas.mixins import EmailSchema
from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
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