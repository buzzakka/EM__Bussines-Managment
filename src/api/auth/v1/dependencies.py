from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from api.auth.v1.utils import exceptions
from src.core.utils import UnitOfWork

from src.api.auth.models import CredentialModel
from api.auth.utils import secret


http_bearer: HTTPBearer = HTTPBearer()


async def get_auth_data(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    try:
        token: str = credentials.credentials
        payload: dict = secret.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise exceptions.incorrect_jwt_token()

    auth_data: dict = {
        'api_key': token,
        'payload': payload
    }

    return auth_data


async def get_current_account(
    auth_data: dict = Depends(get_auth_data)
):
    payload: dict = auth_data.get('payload')

    async with UnitOfWork() as uow:
        credentials: CredentialModel = await uow.credential.get_by_query_one_or_none(
            account_id=payload.get('account_id'),
            api_key=auth_data.get('api_key'),
        )
        if credentials is not None:
            return credentials.account
        raise exceptions.incorrect_jwt_token()
