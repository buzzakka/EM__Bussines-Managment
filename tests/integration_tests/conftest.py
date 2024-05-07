import pytest

from tests.fakes.database.auth_fake_params import (
    FAKE_INVITES,
    FAKE_ACCOUNTS,
    FAKE_COMPANIES,
    FAKE_MEMBER,
    FAKE_SECRETS,
    FAKE_USERS
)

from src.api.auth.models import (
    InviteModel,
    AccountModel,
    SecretModel,
    UserModel,
)
from src.api.company.models import (
    CompanyModel,
    MemberModel
)
from src.core.config import settings


@pytest.fixture(scope='module', autouse=True)
async def fill_db(make_db, async_session_maker) -> None:
    assert settings.MODE == 'TEST'

    fake_data: list = [
        (FAKE_INVITES, InviteModel),
        # (FAKE_ACCOUNTS, AccountModel),
        # (FAKE_COMPANIES, CompanyModel),
        # (FAKE_MEMBER, MemberModel),
        # (FAKE_SECRETS, SecretModel),
        # (FAKE_USERS, UserModel),
    ]
    
    async with async_session_maker() as session:
        for elem in FAKE_INVITES:
            obj = InviteModel(**elem.model_dump())
            session.add(obj)
        await session.commit()

    # async with async_session_maker() as session:
    #     for elem in fake_data:
    #         fake, model = elem
    #         for row in fake:
    #             obj = model(**row.model_dump())
    #             session.add(obj)
    #     await session.commit()
