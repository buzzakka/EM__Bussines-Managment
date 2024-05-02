from pydantic import BaseModel


class NewMemberSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
