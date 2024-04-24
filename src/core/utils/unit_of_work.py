from abc import ABC, abstractmethod

from src.api.auth.v1.repositories.account import AccountRepository
from src.api.auth.v1.repositories.secret import SecretRepository
from src.api.auth.v1.repositories.invite import InviteRepository
from src.api.auth.v1.repositories.user import UserRepository
from src.api.company.v1.repositories.company import CompanyRepository
from src.core.database.db import async_session_maker


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.user = UserRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.secret = SecretRepository(self.session)
        self.account = AccountRepository(self.session)
        self.company = CompanyRepository(self.session)

    async def __aexit__(self, exc_type, *args, **kwargs):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
