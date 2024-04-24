from pydantic import BaseModel


class SecretSchema(BaseModel):
    id: int
    user_id: int
    account_id: int
    password_hash: bytes
