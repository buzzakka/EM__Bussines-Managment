from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.core.schemas import BaseResponseModel
from src.api.router import router

app: FastAPI = FastAPI()

# routers
app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponseModel(
            status_code=exc.status_code,
            error=True,
            message=exc.detail
        ).model_dump()
    )
