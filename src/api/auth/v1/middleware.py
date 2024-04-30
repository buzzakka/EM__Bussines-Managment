from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.utils import UnitOfWork
from src.api.auth import exceptions, utils
from src.api.auth.v1.services import CredentialService


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.scope.get('path') in ['/logout']:
            try:
                payload: dict = self.get_payload(request)
                request.state.payload = payload
            except HTTPException as e:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=e.detail)

        response = await call_next(request)
        return response

    async def get_payload(request: Request) -> dict:
        http_bearer: HTTPBearer = HTTPBearer()
        credential: HTTPAuthorizationCredentials = await http_bearer(request)
        token: str = credential.credentials
        
        is_exist_token: bool = await CredentialService.get_by_query_one_or_none(
            uow=UnitOfWork(),
            api_key=token,
        ) is not None

        if not is_exist_token:
            raise exceptions.incorrect_jwt_token()          
        
        return utils.decode_jwt(token)      
