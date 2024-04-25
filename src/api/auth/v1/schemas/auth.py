from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    passwrod: str
