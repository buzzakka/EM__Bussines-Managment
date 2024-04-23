from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def to_pydantic_schema(self):
        raise NotImplementedError
