from fastapi import HTTPException, Request, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from src.core import exceptions
from src.core.utils import UnitOfWork
from src.api.auth import utils
from src.api.auth.models import CredentialModel
from src.api.auth.v1.services import CredentialService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, 
        router: APIRouter, 
        protected_tag: str = 'protected',
        for_admin_tag: str = 'for_admins',
        *args, 
        **kwargs):
        self.protected_paths: list[str] = [
            route.path for route in router.routes if protected_tag in route.__dict__['tags']
        ]
        self.only_for_admins: list[str] = [
            route.path for route in router.routes if for_admin_tag in route.__dict__['tags']
        ]
        super().__init__(*args, **kwargs)

    async def dispatch(self, request: Request, call_next):
        path: str = request.scope.get('path')
        if path in self.protected_paths:
            try:
                payload: dict = await self._get_payload(request)
                request.state.payload = payload
                
                if path in self.only_for_admins:
                    self._check_is_admin(payload=payload)
            except HTTPException as e:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=e.detail)

        response = await call_next(request)
        return response

    async def _get_payload(self, request: Request) -> dict:
        http_bearer: HTTPBearer = HTTPBearer()
        credential: HTTPAuthorizationCredentials = await http_bearer(request)
        token: str = credential.credentials

        cred_obj: CredentialModel = await CredentialService.get_by_query_one_or_none(
            uow=UnitOfWork(),
            api_key=token,
        )

        if cred_obj is None or not cred_obj.account.is_active:
            raise exceptions.incorrect_jwt_token()

        return utils.decode_jwt(token)
    
    def _check_is_admin(self, payload: dict):
        if not payload['is_admin']:
            raise exceptions.page_not_found()
        
