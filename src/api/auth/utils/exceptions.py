from fastapi import HTTPException, status

from src.api.auth.utils.bad_responses import (
    account_exists_response
)

class AccountAlreadyRegistred(Exception):
    pass


class AccountAlreadyConfirmed(Exception):
    pass


class AccountNotConfirmed(Exception):
    pass


class IvalidInviteToken(Exception):
    pass


class InvalidEmailOrPassword(Exception):
    pass
