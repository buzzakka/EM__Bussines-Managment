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
    )
]


FAKE_ACCOUNTS = [
    AccountSchema(
        id=uuid4(),
        email='user2@example.com',
        is_active=True
    )
]


FAKE_USERS = [
    UserSchema(
        id=uuid4(),
        first_name='Виталий',
        last_name='Артас'
    )
]


FAKE_SECRETS = [
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[0].id,
        account_id=FAKE_ACCOUNTS[0].id,
        password_hash=hash_password('password')
    )
]


