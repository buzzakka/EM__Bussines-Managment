import pytest
from sqlalchemy import select

from tests.fakes.database import (
    FAKE_INVITES,
    FAKE_ACCOUNTS,
    FAKE_USERS,
    FAKE_SECRETS,
    FAKE_MEMBERS,
    FAKE_COMPANYS,
)

from src.api.auth.models import (
    InviteModel,
    AccountModel,
    UserModel,
    SecretModel,
)
from src.api.company.models import (
    MemberModel,
    CompanyModel,
)


@pytest.fixture(scope='session', autouse=True)
async def fill_db(setup_db, async_session_maker) -> None:
    fake_base: list = [
        (FAKE_INVITES, InviteModel),
        (FAKE_ACCOUNTS, AccountModel),
        (FAKE_USERS, UserModel),
        (FAKE_SECRETS, SecretModel),
        (FAKE_MEMBERS, MemberModel),
        (FAKE_COMPANYS, CompanyModel),
    ]

    async with async_session_maker() as s:
        await s.execute(select(InviteModel))
        for elem in fake_base:
            fake, model = elem
            for row in fake:
                obj = model(**row.model_dump())
                s.add(obj)
        await s.commit()