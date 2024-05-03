from fastapi import HTTPException, status


def account_already_registered(email: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Пользователь {email} уже зарегистрирован.'
    )


def incorrect_account_or_invite_token() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный адрес электронной почты или токен.'
    )


def invite_token_already_confirmed() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Почта уже подтверждена.'
    )


def account_is_not_confirmed() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Адрес аэлектронной почты не подтвержден.'
    )


def incorrect_email_or_password() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный логин или пароль.'
    )


def incorrect_email(email: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Пользователь {email} не найден.'
    )


def incorrect_jwt_token() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный переданный JWT токен.'
    )


def page_not_found() -> HTTPException:
    raise HTTPException(
        status_code=404,
        detail='Страница не найдена',
    )


def incorrect_account_id() -> HTTPException:
    raise HTTPException(
        status_code=404,
        detail='Неверный account_id',
    )
