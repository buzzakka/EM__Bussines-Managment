from datetime import datetime
from uuid import uuid4

from tests.fakes.schemas import (
    InviteTestSchema,
    AccountTestSchema,
    UserTestSchema,
    SecretTestSchema,
    MemberTestSchema,
    CompanyTestSchema
)

from src.api.auth.utils import hash_password
from src.api.auth.models.invite import InviteTypes


FAKE_INVITES: list[InviteTestSchema] = [
    InviteTestSchema(
        id=uuid4(),
        email='user_1@example.com',
        token='123456',
        is_confirmed=False,
        invite_type=InviteTypes.ACCOUNT,
    ),
    # InviteTestSchema(
    #     id=uuid4(),
    #     email='user_2@example.com',
    #     token='654321',
    #     is_confirmed=True,
    #     invite_type=InviteTypes.ACCOUNT,
    # ),
    # InviteTestSchema(
    #     id=uuid4(),
    #     email='user_3@example.com',
    #     token='111111',
    #     is_confirmed=True,
    #     invite_type=InviteTypes.ACCOUNT,
    # )
]

FAKE_ACCOUNTS: list[AccountTestSchema] = [
    AccountTestSchema(
        id=uuid4(),
        email='user_3@example.com',
        is_active=True,
    )
]

FAKE_USERS: list[UserTestSchema] = [
    UserTestSchema(
        id=uuid4(),
        first_name='Имя',
        last_name='Фамилия',
    )
]

FAKE_SECRETS: list[SecretTestSchema] = [
    SecretTestSchema(
        id=uuid4(),
        user_id=1,
        account_id=1,
        password_hash=hash_password('qwerty'),
    )
]

FAKE_COMPANIES: list[CompanyTestSchema] = [
    CompanyTestSchema(
        id=uuid4(),
        name='qwerty',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
]

FAKE_MEMBER: list[MemberTestSchema] = [
    MemberTestSchema(
        id=uuid4(),
        account_id=1,
        company_id=1,
        is_admin=True,
    )
]
