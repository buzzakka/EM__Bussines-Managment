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
    # Владелец компании 1
    InviteSchema(
        id=uuid4(),
        email='user_1@example.com',
        token='111111',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=False
    ),

    # Владелец компании 2
    InviteSchema(
        id=uuid4(),
        email='user_2@example.com',
        token='222222',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=True
    ),

    # Пользователи, который подтвердил владение
    InviteSchema(
        id=uuid4(),
        email='user_3@example.com',
        token='333333',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=True
    ),

    InviteSchema(
        id=uuid4(),
        email='user_3_2@example.com',
        token='333333',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=True
    ),

    # Пользователь, который не подтвердил владение
    InviteSchema(
        id=uuid4(),
        email='user_4@example.com',
        token='444444',
        invite_type=InviteTypes.ACCOUNT,
        is_confirmed=False
    ),

    # Работник, подтвердивший владение
    InviteSchema(
        id=uuid4(),
        email='employee_1@example.com',
        token='111111',
        invite_type=InviteTypes.EMPLOYMENT,
        is_confirmed=True
    ),
    # Работник, не подтвердивший владение
    InviteSchema(
        id=uuid4(),
        email='employee_2@example.com',
        token='222222',
        invite_type=InviteTypes.EMPLOYMENT,
        is_confirmed=False
    ),
]


FAKE_ACCOUNTS = [
    AccountSchema(
        id=uuid4(),
        email='user_1@example.com',
        is_active=True
    ),
    AccountSchema(
        id=uuid4(),
        email='user_2@example.com',
        is_active=True
    ),
    AccountSchema(
        id=uuid4(),
        email='employee_1@example.com',
        is_active=False,
    ),
    AccountSchema(
        id=uuid4(),
        email='employee_2@example.com',
        is_active=False,
    ),
]


FAKE_USERS = [
    UserSchema(
        id=uuid4(),
        first_name='Владелец',
        last_name='Аккаунта_1'
    ),
    UserSchema(
        id=uuid4(),
        first_name='Владелец',
        last_name='Аккаунта_2'
    ),
    UserSchema(
        id=uuid4(),
        first_name='Работник',
        last_name='Аккаунта_1'
    ),
    UserSchema(
        id=uuid4(),
        first_name='Работник',
        last_name='Аккаунта_2'
    )

]


FAKE_SECRETS = [
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[0].id,
        account_id=FAKE_ACCOUNTS[0].id,
        password_hash=hash_password('password')
    ),
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[1].id,
        account_id=FAKE_ACCOUNTS[1].id,
        password_hash=hash_password('password')
    ),
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[2].id,
        account_id=FAKE_ACCOUNTS[2].id,
        password_hash=hash_password('password')
    ),
    SecretSchema(
        id=uuid4(),
        user_id=FAKE_USERS[3].id,
        account_id=FAKE_ACCOUNTS[3].id,
        password_hash=hash_password('password')
    ),
]
