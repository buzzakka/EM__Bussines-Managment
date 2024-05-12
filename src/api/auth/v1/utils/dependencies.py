from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.core.utils import UnitOfWork

from src.api.auth.utils import secret, bad_responses


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login/'
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload: dict = secret.decode_jwt(token=token)
    except InvalidTokenError:
        raise bad_responses.not_authenticated()
    return payload


async def is_authenticated_user(
    payload: dict = Depends(get_current_token_payload)
):
    async with UnitOfWork() as uow:
        current_user = await uow.account.get_by_query_one_or_none(
            id=payload['account_id'], is_active=True
        )
        if current_user is None:
            raise bad_responses.not_authenticated()

        return payload


def is_admin(
    payload: dict = Depends(is_authenticated_user)
):
    if not payload['is_admin']:
        raise bad_responses.forbidden()

    return payload
