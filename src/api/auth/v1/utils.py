from datetime import datetime
import bcrypt
import jwt

from src.core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt_auth_settings.private_key_path.read_text(),
    algorithm: str = settings.jwt_auth_settings.algorithm,
) -> str:
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_auth_settings.public_key_path.read_text(),
    algorithm: str = settings.jwt_auth_settings.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )
    return decoded


def hash_password(
    password: str
) -> bytes:
    salt: bytes = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )


def make_payload(
    account_id: int,
    email: str,
    created_at: datetime = datetime.now()
) -> dict:
    payload: dict = {
        'account_id': account_id,
        'email': email,
        'created_at': created_at
    }
    return payload
