from uuid import uuid4

from tests.fakes.schemas import (
    CompanySchema,
    MemberSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS
from src.api.auth.models import InviteTypes
from src.api.auth.utils import hash_password


FAKE_COMPANYS = [
    CompanySchema(
        id=uuid4(),
        name='users2 company'
    )
]


FAKE_MEMBERS = [
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[0].id,
        company_id=FAKE_COMPANYS[0].id,
        is_admin=True
    )
]
