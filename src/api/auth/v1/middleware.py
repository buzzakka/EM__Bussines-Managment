from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.auth.v1 import utils


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.scope.get('path') in ['/logout']:
            http_bearer: HTTPBearer = HTTPBearer()
            try:
                credential: HTTPAuthorizationCredentials = await http_bearer(request)
                token: str = credential.credentials
                utils.decode_jwt(token)
            except HTTPException as e:
                return JSONResponse(status_code=401, content=e.detail)

        response = await call_next(request)    
        return response
    
    @staticmethod
    async def is_valid_token(token: str):
        payload: dict = utils.decode_jwt(token)        
