import logging
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


from src import models
from src.exceptions.authentication import AuthenticationException
from src.exceptions.user import UserException
from src.views.health import router as health_router
from src.views.user import router as user_router

def create_app():
    app = FastAPI(title="Studing ticket", debug=False)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": str(exc)},
        )

    app.include_router(
        health_router,
        prefix="/api",
        tags=["Health check"]
    )

    app.include_router(
        user_router,
        prefix="/api",
        tags=["User"]
    )

    return app
