from src.core.utils import BaseService, UnitOfWork
from api.auth import utils


class CredentialService(BaseService):
    repository: str = 'credential'

    @classmethod
    async def add_token(cls, uow: UnitOfWork, email: str):
        async with uow:
            db_payload = await uow.credential.get_payload(email=email)
            payload: dict = utils.make_payload(
                account_id=db_payload.account_id,
                company_id=db_payload.company_id,
                is_admin=db_payload.is_admin
            )

            token: str = utils.encode_jwt(payload=payload)

            filters: dict = {'account_id': payload['account_id']}
            values: dict = {
                'account_id': payload['account_id'],
                'api_key': token,
            }

            await uow.credential.update_one_or_create_new(
                filters=filters,
                values=values,
            )

        return token
