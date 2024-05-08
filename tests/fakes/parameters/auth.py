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
from src.api.auth.schemas import (
    UserLoginRequestSchema,
    UserLoginResponseSchema,
    TokenSchema
)


TEST_ENDPOINT_CHECK_ACCOUNT: list[tuple[any]] = [
    # Проверка аккаунта нового пользователя
    (
        'fake_user_1@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(
            email='fake_user_1@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Проверка аккаунта у пользователя, который уже проверял его
    (
        'fake_user_1@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(
            email='fake_user_1@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Проверка аккаунта у пользователя, который уже подтвердил его
    (
        'user_3@example.com',
        CheckAccountResponseSchema(payload=EmailSchema(
            email='user_3@example.com')).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Проверка аккаунта у зарегестрированного пользователя
    (
        'user_1@example.com',
        CheckAccountResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user_1@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPANY: list[tuple[any]] = [
    # Подтверждение корректного инвайт токена
    (
        SignUpRequestSchema(
            account='user_4@example.com',
            invite_token='444444'
        ).model_dump(),
        SignUpResponseSchema(
            payload=EmailSchema(email='user_4@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Подтверждение некорректного инвайт токена
    (
        SignUpRequestSchema(
            account='fake_user_1@example.com', invite_token='qwerty'
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
            account='qwe@qwe.qwe', invite_token='qwerty'
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
            account='user_3_2@example.com', invite_token='333333'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт user_3_2@example.com уже подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Подтверждение уже зарегестрированного аккаунта
    (
        SignUpRequestSchema(
            account='user_1@example.com', invite_token='111111'
        ).model_dump(),
        SignUpResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user_1@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPLETE_COMPANY: list[tuple[any]] = [
    # Регистрация нового пользователя
    (
        AccountRegisterRequestSchema(
            account='user_3@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            payload=AccountRegisterPayload(
                account='user_3@example.com',
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
            account='fake_user@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт fake_user@example.com не подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Регистрация зарегестрированного
    (
        AccountRegisterRequestSchema(
            account='user_2@example.com',
            first_name='Alan',
            last_name='Wake',
            company_name='Remedy',
            password='password'
        ).model_dump(),
        AccountRegisterResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь user_2@example.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

]

TEST_ENDPOINT_CONFIRM_EMPLOYEE_ACCOUNT: list[tuple[any]] = [
    # Попытка подтверждения с неправильным токеном
    (
        'employee_2@example.com',
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
        'employee_2@example.com',
        '222222',
        EmployeConfirmResponseSchema(
            payload=EmailSchema(email='employee_2@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Попытка подтверждения подтвержденного пользователя
    (
        'employee_1@example.com',
        '111111',
        EmployeConfirmResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт employee_1@example.com уже подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_SIGN_UP_COMPLETE_EMPLOYEE: list[tuple[any]] = [
    # Регистрация пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='employee_1@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            payload=EmailSchema(email='employee_1@example.com')
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Повторная попытка регистрации пользователя
    (
        EmployeeSignUpCompleteRequestSchema(
            email='employee_1@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь employee_1@example.com уже зарегистрирован.'
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
            email='employee_2@example.com', password='password'
        ).model_dump(),
        EmployeeSignUpCompleteResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Аккаунт employee_2@example.com не подтвержден.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_INVALID_TOKEN: list[tuple[any]] = [
    (
        UserLoginRequestSchema(email='error@example.com',
                               password='qwe').model_dump(),
        UserLoginResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный адрес электронной почты или пароль.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    )
]
