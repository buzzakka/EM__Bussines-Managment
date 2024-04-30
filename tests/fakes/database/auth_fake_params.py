from datetime import datetime

from src.api.auth.schemas import (
    InviteSchema,
    AccountSchema,
    UserSchema,
    SecretSchema,
)
from src.api.company.schemas import (
    CompanySchema,
    MemberSchema,
)
from api.auth.utils import hash_password


FAKE_INVITES: list[InviteSchema] = [
    InviteSchema(
        email='user_1@example.com',
        token='123456',
        is_confirmed=False,
        created_at=datetime.now(),
        invite_type='registration',
    ),
    InviteSchema(
        email='user_2@example.com',
        token='654321',
        is_confirmed=True,
        created_at=datetime.now(),
        invite_type='registration',
    ),
    InviteSchema(
        email='user_3@example.com',
        token='111111',
        is_confirmed=True,
        created_at=datetime.now(),
        invite_type='registration',
    )
]

FAKE_ACCOUNTS: list[AccountSchema] = [
    AccountSchema(
        email='user_3@example.com',
        is_active=True,
    )
]

FAKE_USERS: list[UserSchema] = [
    UserSchema(
        first_name='Имя',
        last_name='Фамилия',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
]

FAKE_SECRETS: list[SecretSchema] = [
    SecretSchema(
        user_id=1,
        account_id=1,
        password_hash=hash_password('qwerty'),
    )
]

FAKE_COMPANIES: list[CompanySchema] = [
    CompanySchema(
        name='qwerty',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
]

FAKE_MEMBER: list[MemberSchema]  = [
    MemberSchema(
        account_id=1,
        company_id=1,
        is_admin=True,
    )
]
