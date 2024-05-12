from fastapi import HTTPException, status


def account_exists_response():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Пользователь с таким адресом электронной почты уже зарегестрирован.'
    )


def account_confirmed_already():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Аккаунт уже подтвержден.'
    )


def account_not_confirmed():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Аккаунт не подтвержден.'
    )


def invalid_email_or_ivite_token():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный адрес электронной почты или токен.'
    )


def invalid_email_or_password():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный адрес электронной почты или пароль.'
    )


def not_authenticated():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Not authenticated'
    )


def forbidden():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Страница недоступна.'
    )
