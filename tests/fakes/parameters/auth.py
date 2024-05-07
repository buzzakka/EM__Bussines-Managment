from contextlib import nullcontext as does_not_raise
from fastapi import status

from src.api.auth.schemas.mixins import EmailSchema
from src.api.auth.v1.schemas import (
    CheckAccountResponseSchema,
    
    SignUpRequestSchema,
    SignUpResponseSchema,
    
    AccountRegisterPayload,
    AccountRegisterRequestSchema,
    AccountRegisterResponseSchema,
    
    EmployeConfirmResponseSchema,
    
    EmployeeSignUpCompleteRequestSchema,
    EmployeeSignUpCompleteResponseSchema,
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
            message='Неверный адрес электронной почты или токен.'
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
            message='Неверный адрес электронной почты или токен.'
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
    # Регистрация нового пользователя
    (
        AccountRegisterRequestSchema(
            account='user4@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            payload=AccountRegisterPayload(
                account='user4@example.com',
                first_name='Alan',
                last_name='Wake',
                company_name='Remedy',
            )
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Регистрация пользователя с неподтвержденным email
    (
        AccountRegisterRequestSchema(
            account='user@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт user@example.com не подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Регистрация зарегестрированного
    (
        AccountRegisterRequestSchema(
            account='user4@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user4@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

]

TEST_ENDPOINT_CONFIRM_EMPLOYEE_ACCOUTN: list[tuple[any]] = [
    # Попытка подтверждения с неправильным токеном
    (
        'employee@example.com',
        'token',
        EmployeConfirmResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный адрес электронной почты или токен.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Попытка подтверждения с несуществующей почты
    (
        'error@error.com',
        'token',
        EmployeConfirmResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный адрес электронной почты или токен.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Успешная попытка подтверждения
    (
        'employee@example.com',
        '333333',
        EmployeConfirmResponseSchema(
            payload=EmailSchema(email='employee@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Попытка подтверждения подтвержденного пользователя
    (
        'employee@example.com',
        '333333',
        EmployeConfirmResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт employee@example.com уже подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPLETE_EMPLOYEE: list[tuple[any]] = [
    # Регистрация пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='employee_2@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            payload=EmailSchema(email='employee_2@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Повторная попытка регистрации пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='employee_2@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь employee_2@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Попытка регистрации несуществующего пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='error@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт error@example.com не подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Попытка регистрации неподтвержденного пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='employee@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт employee@example.com не подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]
