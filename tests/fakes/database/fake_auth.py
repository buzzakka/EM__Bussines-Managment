from uuid import uuid4

from tests.fakes.schemas import (
    InviteSchema,
    AccountSchema,
    SecretSchema,
    UserSchema
)
from src.api.auth.models import InviteTypes
from api.auth.utils.secret import hash_password


FAKE_INVITES = [
    InviteSchema(
        id=uuid4(),
        email='user1@example.com',
        token='111111',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=False
    ),
    InviteSchema(
        id=uuid4(),
        email='user2@example.com',
        token='222222',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=True
    ),
    InviteSchema(
        id=uuid4(),
        email='user3@example.com',
        token='222222',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=True
    ),
    InviteSchema(
        id=uuid4(),
        email='user4@example.com',
        token='222222',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=False
    ),
    InviteSchema(
        id=uuid4(),
        email='employee@example.com',
        token='333333',
        invite_type=InviteTypes.EMPLOYMENT,
        is_confirmed=False
    ),
    InviteSchema(
        id=uuid4(),
        email='employee_2@example.com',
        token='444444',
        invite_type=InviteTypes.EMPLOYMENT,
        is_confirmed=True
    )
]


FAKE_ACCOUNTS = [
    AccountSchema(
        id=uuid4(),
        email='user2@example.com',
        is_active=True
    ),
    AccountSchema(
        id=uuid4(),
        email='employee_2@example.com',
        is_active=False,
    )
]


FAKE_USERS = [
    UserSchema(
        id=uuid4(),
        first_name='Виталий',
        last_name='Артас'
    ),
    UserSchema(
        id=uuid4(),
        first_name='Работник',
        last_name='Юниттестовый'
    )
]


FAKE_SECRETS = [
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[0].id,
        account_id=FAKE_ACCOUNTS[0].id,
        password_hash=hash_password('password')
    ),
    # SecretSchema(
    #     id=uuid4(),

    # )
]
