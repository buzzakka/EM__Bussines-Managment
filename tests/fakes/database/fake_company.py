from uuid import uuid4

from tests.fakes.schemas import (
    CompanySchema,
    MemberSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS


FAKE_COMPANYS = [
    CompanySchema(
        id=uuid4(),
        name='user_1@example.com company'
    ),
    CompanySchema(
        id=uuid4(),
        name='user_2@example.com company'
    )
]


FAKE_MEMBERS = [
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[0].id,
        company_id=FAKE_COMPANYS[0].id,
        is_admin=True
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[2].id,
        company_id=FAKE_COMPANYS[0].id,
        is_admin=False
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[1].id,
        company_id=FAKE_COMPANYS[1].id,
        is_admin=True
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[3].id,
        company_id=FAKE_COMPANYS[1].id,
        is_admin=False
    ),
]
