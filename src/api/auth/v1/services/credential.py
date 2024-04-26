from datetime import datetime
from src.core.utils import BaseService, UnitOfWork
from src.api.auth.v1.models import SecretModel
from src.api.auth.v1.utils import encode_jwt, make_payload


class CredentialService(BaseService):
    repository: str = 'credential'

    @classmethod
    async def add_token(cls, uow: UnitOfWork, secret: SecretModel, email: str):
        created_at: datetime = datetime.now()
        payload: dict = make_payload(
            account_id=secret.account_id,
            email=email,
            created_at=str(created_at)
        )
        token: str = encode_jwt(payload=payload)

        filters: dict = {'account_id': secret.account_id}
        values: dict = {
            'account_id': secret.account_id,
            'created_at': created_at,
            'api_key': token,
        }

        await cls.update_one_or_create_new(
            uow=uow,
            filters=filters,
            values=values,
        )

        return token
