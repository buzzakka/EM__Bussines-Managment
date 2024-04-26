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
    iat: datetime
) -> dict:
    payload: dict = {
        'account_id': account_id,
        'email': email,
        'iat': iat
    }
    return payload


# def get_current_token_payload(
#     credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
# ):
#     token: str = credentials.credentials
#     payload = decode_jwt(token)
#     return payload


# def get_current_user(
#     payload: dict = Depends(get_current_token_payload)
# ):
#     account_id: int = payload.get('sub')
#     user = 
